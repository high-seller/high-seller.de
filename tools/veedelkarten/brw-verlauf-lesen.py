#!/usr/bin/env python3
"""Bodenrichtwert-Verlauf je Zone über mehrere Jahrgänge.

Das ist die eigentlich seltene Information: BORIS NRW veröffentlicht die
Bodenrichtwerte seit 2011, aber niemand bereitet sie stadtteilweise als
Zeitreihe auf. Der Wert einer einzelnen Zone über fünfzehn Jahre steht so
nirgends im Netz.

Zugeordnet wird über den Ort, nicht über die Zonennummer: Zonen werden
gelegentlich neu geschnitten und umnummeriert. Für jede Zone des aktuellen
Jahrgangs wird ein Punkt im Inneren bestimmt und im alten Jahrgang gesucht,
welches Polygon diesen Punkt enthält.
"""
import json
import math
import os
import struct
import zipfile

TMP = os.path.dirname(os.path.abspath(__file__))
JAHRE = [2011, 2015, 2019, 2023, 2024, 2025]

A = 6378137.0
F = 1 / 298.257222101
E2 = F * (2 - F)
K0, OST0 = 0.9996, 500000.0
LAMBDA0 = math.radians(9.0)


def wgs_nach_utm(lon, lat):
    phi, lam = math.radians(lat), math.radians(lon)
    n = A / math.sqrt(1 - E2 * math.sin(phi) ** 2)
    t = math.tan(phi) ** 2
    c = E2 / (1 - E2) * math.cos(phi) ** 2
    aa = math.cos(phi) * (lam - LAMBDA0)
    m = A * ((1 - E2/4 - 3*E2**2/64 - 5*E2**3/256) * phi
             - (3*E2/8 + 3*E2**2/32 + 45*E2**3/1024) * math.sin(2*phi)
             + (15*E2**2/256 + 45*E2**3/1024) * math.sin(4*phi)
             - (35*E2**3/3072) * math.sin(6*phi))
    ost = OST0 + K0 * n * (aa + (1-t+c)*aa**3/6
                           + (5-18*t+t**2+72*c-58*E2/(1-E2))*aa**5/120)
    nord = K0 * (m + n*math.tan(phi) * (aa**2/2 + (5-t+9*c+4*c**2)*aa**4/24
                 + (61-58*t+t**2+600*c-330*E2/(1-E2))*aa**6/720))
    return ost, nord


def im_polygon(px, py, ring):
    """Strahlverfahren."""
    drin = False
    n = len(ring)
    for i in range(n):
        x1, y1 = ring[i]
        x2, y2 = ring[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            xs = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if px < xs:
                drin = not drin
    return drin


def dbf_lesen(pfad):
    with open(pfad, "rb") as f:
        kopf = f.read(32)
        anzahl, kopflaenge, satzlaenge = struct.unpack("<I H H", kopf[4:12])
        felder, pos = [], 32
        while True:
            f.seek(pos)
            b = f.read(32)
            if not b or b[0] == 0x0D:
                break
            felder.append((b[:11].split(b"\x00")[0].decode("utf-8", "replace"), b[16]))
            pos += 32
    return anzahl, kopflaenge, satzlaenge, felder


def satz(f, nr, kopflaenge, satzlaenge, felder):
    f.seek(kopflaenge + nr * satzlaenge)
    b = f.read(satzlaenge)
    aus, pos = {}, 1
    for name, laenge in felder:
        aus[name] = b[pos:pos + laenge].decode("utf-8", "replace").strip()
        pos += laenge
    return aus


def jahrgang_lesen(jahr, suchpunkte, box):
    """Gibt je Suchpunkt den Bodenrichtwert des enthaltenden Polygons."""
    zip_pfad = os.path.join(TMP, "boris-jahre", f"{jahr}.zip")
    z = zipfile.ZipFile(zip_pfad)
    shp_name = next(n for n in z.namelist() if n.lower().endswith(".shp"))
    dbf_name = next(n for n in z.namelist() if n.lower().endswith(".dbf"))
    ordner = os.path.join(TMP, "boris-jahre", str(jahr))
    os.makedirs(ordner, exist_ok=True)
    for n in (shp_name, dbf_name):
        ziel = os.path.join(ordner, os.path.basename(n))
        if not os.path.exists(ziel):
            with z.open(n) as q, open(ziel, "wb") as w:
                while True:
                    stueck = q.read(1 << 20)
                    if not stueck:
                        break
                    w.write(stueck)

    shp = os.path.join(ordner, os.path.basename(shp_name))
    dbf = os.path.join(ordner, os.path.basename(dbf_name))
    anzahl, kopflaenge, satzlaenge, felder = dbf_lesen(dbf)
    namen = [n for n, _ in felder]
    feld_brw = "BRW" if "BRW" in namen else None
    feld_entw = "ENTW" if "ENTW" in namen else None

    treffer = {}
    with open(shp, "rb") as f, open(dbf, "rb") as fd:
        f.seek(100)
        nr = 0
        while True:
            kopf = f.read(8)
            if len(kopf) < 8:
                break
            _, laenge = struct.unpack(">i i", kopf)
            inhalt = f.read(laenge * 2)
            nr += 1
            if len(inhalt) < 44 or struct.unpack("<i", inhalt[:4])[0] != 5:
                continue
            xmin, ymin, xmax, ymax = struct.unpack("<4d", inhalt[4:36])
            if xmax < box[0] or xmin > box[2] or ymax < box[1] or ymin > box[3]:
                continue
            offen = [(k, p) for k, p in suchpunkte.items()
                     if k not in treffer and xmin <= p[0] <= xmax and ymin <= p[1] <= ymax]
            if not offen:
                continue
            n_teile, n_punkte = struct.unpack("<i i", inhalt[36:44])
            teile = struct.unpack(f"<{n_teile}i", inhalt[44:44 + n_teile*4])
            p0 = 44 + n_teile * 4
            roh = struct.unpack(f"<{n_punkte*2}d", inhalt[p0:p0 + n_punkte*16])
            grenzen = list(teile) + [n_punkte]
            ringe = [[(roh[j*2], roh[j*2+1]) for j in range(grenzen[i], grenzen[i+1])]
                     for i in range(n_teile)]
            for k, p in offen:
                if any(im_polygon(p[0], p[1], r) for r in ringe if len(r) > 3):
                    d = satz(fd, nr - 1, kopflaenge, satzlaenge, felder)
                    if feld_entw and d.get(feld_entw) != "B":
                        continue
                    try:
                        treffer[k] = int(d[feld_brw])
                    except (ValueError, KeyError, TypeError):
                        pass
    return treffer


def main():
    aus = {}
    for stadtteil, datei in (("deutz", "boris-deutz.json"), ("suelz", "boris-suelz.json")):
        zonen = [z for z in json.load(open(os.path.join(TMP, datei), encoding="utf-8"))
                 if z["daten"].get("ENTW") == "B"]
        if stadtteil == "suelz":
            zonen = [z for z in zonen if z["daten"].get("ORTST") == "Sülz"]
        else:
            zonen = [z for z in zonen if z["daten"].get("ORTST") == "Deutz"]

        punkte, stamm = {}, {}
        for z in zonen:
            ring = max(z["ringe"], key=len)
            # Schwerpunkt, notfalls ein echter Innenpunkt
            mx = sum(p[0] for p in ring) / len(ring)
            my = sum(p[1] for p in ring) / len(ring)
            if not im_polygon(mx, my, ring):
                mx, my = ring[len(ring) // 3]
                mx += 1e-5
            schluessel = z["daten"].get("BRWZNR") or str(id(z))
            punkte[schluessel] = wgs_nach_utm(mx, my)
            stamm[schluessel] = {
                "brw2026": int(z["daten"]["BRW"]),
                "lage": z["daten"].get("BEM", ""),
                "nutzung": z["daten"].get("NUTA", ""),
            }

        xs = [p[0] for p in punkte.values()]
        ys = [p[1] for p in punkte.values()]
        box = (min(xs) - 50, min(ys) - 50, max(xs) + 50, max(ys) + 50)

        reihe = {k: {"2026": v["brw2026"], **{}} for k, v in stamm.items()}
        for jahr in JAHRE:
            gefunden = jahrgang_lesen(jahr, punkte, box)
            for k, w in gefunden.items():
                reihe[k][str(jahr)] = w
            print(f"  {stadtteil} {jahr}: {len(gefunden)}/{len(punkte)} Zonen zugeordnet")

        aus[stadtteil] = {k: {**stamm[k], "reihe": reihe[k]} for k in stamm}

    json.dump(aus, open(os.path.join(TMP, "brw-verlauf.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("→ brw-verlauf.json")


if __name__ == "__main__":
    main()
