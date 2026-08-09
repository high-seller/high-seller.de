#!/usr/bin/env python3
"""Liest die Bodenrichtwertzonen für Köln-Deutz aus dem BORIS-Shapefile.

Der Landesdatensatz umfasst ganz Nordrhein-Westfalen (290 MB Geometrie,
109 MB Sachdaten). Weder geopandas noch pyshp oder GDAL stehen hier zur
Verfügung, deshalb liest dieses Skript beide Formate direkt: Das
Shapefile-Format ist offen dokumentiert und für Polygone überschaubar.

Gelesen wird streamend über den .shx-Index, damit nie die ganze Datei im
Speicher liegt. Die Umrechnung von ETRS89/UTM32 nach WGS84 steckt unten und
folgt der üblichen Reihenentwicklung; auf wenigen Kilometern Ausdehnung liegt
der Fehler weit unter einem Meter.
"""
import json
import math
import os
import struct

TMP = os.path.dirname(os.path.abspath(__file__))
SHP = os.path.join(TMP, "boris", "BRW_2026_Polygon.shp")
DBF = os.path.join(TMP, "boris", "BRW_2026_Polygon.dbf")

# Kartenausschnitt in WGS84 mit etwas Rand
LON0, LON1 = 6.9560, 7.0040
LAT0, LAT1 = 50.9300, 50.9500


# --- UTM32 (ETRS89) nach WGS84 -------------------------------------------
A = 6378137.0
F = 1 / 298.257222101
E2 = F * (2 - F)
E1 = (1 - math.sqrt(1 - E2)) / (1 + math.sqrt(1 - E2))
K0 = 0.9996
OST0 = 500000.0
LAMBDA0 = math.radians(9.0)   # Zentralmeridian Zone 32


def utm_nach_wgs84(ost, nord):
    x = ost - OST0
    m = nord / K0
    mu = m / (A * (1 - E2 / 4 - 3 * E2**2 / 64 - 5 * E2**3 / 256))
    phi1 = (mu
            + (3 * E1 / 2 - 27 * E1**3 / 32) * math.sin(2 * mu)
            + (21 * E1**2 / 16 - 55 * E1**4 / 32) * math.sin(4 * mu)
            + (151 * E1**3 / 96) * math.sin(6 * mu)
            + (1097 * E1**4 / 512) * math.sin(8 * mu))
    sin1, cos1, tan1 = math.sin(phi1), math.cos(phi1), math.tan(phi1)
    n1 = A / math.sqrt(1 - E2 * sin1**2)
    t1 = tan1**2
    ep2 = E2 / (1 - E2)
    c1 = ep2 * cos1**2
    r1 = A * (1 - E2) / (1 - E2 * sin1**2) ** 1.5
    d = x / (n1 * K0)

    lat = phi1 - (n1 * tan1 / r1) * (
        d**2 / 2
        - (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * ep2) * d**4 / 24
        + (61 + 90 * t1 + 298 * c1 + 45 * t1**2 - 252 * ep2 - 3 * c1**2) * d**6 / 720)
    lon = LAMBDA0 + (
        d
        - (1 + 2 * t1 + c1) * d**3 / 6
        + (5 - 2 * c1 + 28 * t1 - 3 * c1**2 + 8 * ep2 + 24 * t1**2) * d**5 / 120) / cos1
    return math.degrees(lon), math.degrees(lat)


def wgs84_nach_utm(lon, lat):
    """Nur für die Suchbox — grobe Umkehrung reicht, sie wird großzügig gewählt."""
    phi = math.radians(lat)
    lam = math.radians(lon)
    n = A / math.sqrt(1 - E2 * math.sin(phi) ** 2)
    t = math.tan(phi) ** 2
    c = E2 / (1 - E2) * math.cos(phi) ** 2
    aa = math.cos(phi) * (lam - LAMBDA0)
    m = A * ((1 - E2 / 4 - 3 * E2**2 / 64 - 5 * E2**3 / 256) * phi
             - (3 * E2 / 8 + 3 * E2**2 / 32 + 45 * E2**3 / 1024) * math.sin(2 * phi)
             + (15 * E2**2 / 256 + 45 * E2**3 / 1024) * math.sin(4 * phi)
             - (35 * E2**3 / 3072) * math.sin(6 * phi))
    ost = OST0 + K0 * n * (aa + (1 - t + c) * aa**3 / 6
                           + (5 - 18 * t + t**2 + 72 * c - 58 * E2 / (1 - E2)) * aa**5 / 120)
    nord = K0 * (m + n * math.tan(phi) * (aa**2 / 2 + (5 - t + 9 * c + 4 * c**2) * aa**4 / 24
                 + (61 - 58 * t + t**2 + 600 * c - 330 * E2 / (1 - E2)) * aa**6 / 720))
    return ost, nord


ecken = [wgs84_nach_utm(x, y) for x in (LON0, LON1) for y in (LAT0, LAT1)]
OST_MIN = min(e[0] for e in ecken) - 300
OST_MAX = max(e[0] for e in ecken) + 300
NORD_MIN = min(e[1] for e in ecken) - 300
NORD_MAX = max(e[1] for e in ecken) + 300
print(f"Suchbereich UTM32: Ost {OST_MIN:.0f}–{OST_MAX:.0f}, Nord {NORD_MIN:.0f}–{NORD_MAX:.0f}")


# --- DBF-Sachdaten --------------------------------------------------------
def dbf_kopf(pfad):
    with open(pfad, "rb") as f:
        kopf = f.read(32)
        anzahl, kopflaenge, satzlaenge = struct.unpack("<I H H", kopf[4:12])
        felder = []
        pos = 32
        while True:
            f.seek(pos)
            b = f.read(32)
            if not b or b[0] == 0x0D:
                break
            name = b[:11].split(b"\x00")[0].decode("utf-8", "replace")
            typ = chr(b[11])
            laenge = b[16]
            felder.append((name, typ, laenge))
            pos += 32
    return anzahl, kopflaenge, satzlaenge, felder


anzahl, kopflaenge, satzlaenge, felder = dbf_kopf(DBF)
print(f"DBF: {anzahl} Datensätze, {len(felder)} Felder")
print("Felder:", ", ".join(f"{n}({t})" for n, t, _ in felder[:28]))


def dbf_satz(f, nr):
    f.seek(kopflaenge + nr * satzlaenge)
    b = f.read(satzlaenge)
    aus = {}
    pos = 1
    for name, typ, laenge in felder:
        # Die .cpg-Datei weist UTF-8 aus; latin-1 zerlegt die Umlaute.
        aus[name] = b[pos:pos + laenge].decode("utf-8", "replace").strip()
        pos += laenge
    return aus


# --- SHP streamend lesen --------------------------------------------------
treffer = []
with open(SHP, "rb") as f, open(DBF, "rb") as fd:
    f.seek(100)
    nr = 0
    while True:
        kopf = f.read(8)
        if len(kopf) < 8:
            break
        _, laenge = struct.unpack(">i i", kopf)
        inhalt = f.read(laenge * 2)
        nr += 1
        if len(inhalt) < 44:
            continue
        typ = struct.unpack("<i", inhalt[:4])[0]
        if typ != 5:
            continue
        xmin, ymin, xmax, ymax = struct.unpack("<4d", inhalt[4:36])
        if xmax < OST_MIN or xmin > OST_MAX or ymax < NORD_MIN or ymin > NORD_MAX:
            continue
        n_teile, n_punkte = struct.unpack("<i i", inhalt[36:44])
        teile = struct.unpack(f"<{n_teile}i", inhalt[44:44 + n_teile * 4])
        p0 = 44 + n_teile * 4
        roh = struct.unpack(f"<{n_punkte * 2}d", inhalt[p0:p0 + n_punkte * 16])
        ringe = []
        grenzen = list(teile) + [n_punkte]
        for i in range(n_teile):
            ring = []
            for j in range(grenzen[i], grenzen[i + 1]):
                lon, lat = utm_nach_wgs84(roh[j * 2], roh[j * 2 + 1])
                ring.append((round(lon, 6), round(lat, 6)))
            if len(ring) > 3:
                ringe.append(ring)
        if ringe:
            treffer.append({"nr": nr - 1, "ringe": ringe})

    print(f"{len(treffer)} Zonen im Suchbereich")
    for t in treffer:
        t["daten"] = dbf_satz(fd, t["nr"])

json.dump(treffer, open(os.path.join(TMP, "boris-deutz.json"), "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))
print("→ boris-deutz.json")
if treffer:
    print("\nBeispiel-Attribute:")
    for k, v in list(treffer[0]["daten"].items()):
        if v:
            print(f"    {k:14} {v[:44]}")
