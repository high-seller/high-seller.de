#!/usr/bin/env python3
"""Liest die OSM-Rohdaten und schreibt die Kartenebenen als kompaktes JSON.

Die Rohdateien kommen von der OSM-Hauptschnittstelle (/api/0.6/map). Der Weg
über die Overpass-API war nicht gangbar: Sie lief bei fast jeder größeren
Abfrage in Zeitüberschreitungen und Ratenbegrenzungen.

Herausgeschrieben wird nur, was die Karte zeichnet — aus 27 MB XML werden
wenige hundert Kilobyte.
"""
import json
import os
import xml.etree.ElementTree as ET

TMP = os.path.dirname(os.path.abspath(__file__))
DATEIEN = ["karte-roh.osm", "karte-roh2.osm"]

# Kartenausschnitt; alles, was komplett draußen liegt, fliegt sofort raus.
LAT0, LAT1 = 50.9332, 50.9468
LON0, LON1 = 6.9602, 6.9992

STRASSEN_RANG = {
    "motorway": 1, "trunk": 1, "primary": 2, "secondary": 3,
    "tertiary": 4, "residential": 5, "unclassified": 5, "living_street": 5,
}


def einlesen(pfad):
    """Gibt die getaggten Wege zurueck und zusaetzlich die Wege, die als
    Aussenring einer Wasser-Relation dienen. Letztere tragen meist selbst
    keine Tags — genau daran ist der erste Anlauf gescheitert und der Rhein
    fehlte in der Karte."""
    knoten = {}
    alle_wege = {}
    wege = []
    wurzel = ET.parse(pfad).getroot()
    for k in wurzel.iter("node"):
        knoten[k.get("id")] = (float(k.get("lon")), float(k.get("lat")))
    for w in wurzel.iter("way"):
        punkte = [knoten[nd.get("ref")] for nd in w.findall("nd")
                  if nd.get("ref") in knoten]
        if len(punkte) < 2:
            continue
        alle_wege[w.get("id")] = punkte
        tags = {t.get("k"): t.get("v") for t in w.findall("tag")}
        if tags:
            wege.append((tags, punkte))

    for r in wurzel.iter("relation"):
        tags = {t.get("k"): t.get("v") for t in r.findall("tag")}
        if tags.get("natural") != "water" and tags.get("waterway") != "riverbank":
            continue
        for m in r.findall("member"):
            if m.get("type") == "way" and m.get("role") in ("outer", ""):
                punkte = alle_wege.get(m.get("ref"))
                if punkte:
                    wege.append(({"natural": "water", "_ausRelation": "1"}, punkte))
    return wege


def beruehrt(punkte):
    return any(LON0 - 0.002 <= x <= LON1 + 0.002 and LAT0 - 0.002 <= y <= LAT1 + 0.002
               for x, y in punkte)


def runden(punkte, stellen=5):
    """Fünf Nachkommastellen sind rund ein Meter — mehr braucht die Karte nicht
    und es spart die Hälfte der Dateigröße."""
    aus = []
    for x, y in punkte:
        p = (round(x, stellen), round(y, stellen))
        if not aus or p != aus[-1]:
            aus.append(p)
    return aus


ebenen = {"wasser": [], "ufer": [], "gebaeude": [], "strassen": [], "bahn": [],
          "gruen": [], "bruecken": [], "platz": []}

for datei in DATEIEN:
    pfad = os.path.join(TMP, datei)
    if not os.path.exists(pfad):
        continue
    for tags, punkte in einlesen(pfad):
        if not beruehrt(punkte):
            continue
        p = runden(punkte)
        if len(p) < 2:
            continue

        name = tags.get("name", "")

        if tags.get("natural") == "water" or tags.get("waterway") == "riverbank" \
                or tags.get("water") == "river":
            xs = [q[0] for q in p]; ys = [q[1] for q in p]
            gross = (max(xs) - min(xs)) > 0.0012 or (max(ys) - min(ys)) > 0.0012
            if tags.get("_ausRelation"):
                ebenen["ufer"].append(p)
            elif gross:
                ebenen["wasser"].append(p)
            continue

        if tags.get("building"):
            xs = [q[0] for q in p]; ys = [q[1] for q in p]
            # Winzige Nebengebäude weglassen, sonst wird die Karte zu Grieß.
            if (max(xs) - min(xs)) > 0.00018 or (max(ys) - min(ys)) > 0.00018:
                ebenen["gebaeude"].append(p)
            continue

        if tags.get("railway") in ("rail", "light_rail") and \
                tags.get("service") not in ("yard", "siding", "spur"):
            ebenen["bahn"].append(p)
            continue

        if tags.get("leisure") in ("park", "garden", "pitch", "playground") or \
                tags.get("landuse") in ("grass", "recreation_ground", "cemetery", "forest") or \
                tags.get("natural") in ("scrub", "wood", "grassland"):
            ebenen["gruen"].append({"p": p, "n": name})
            continue

        if tags.get("place") == "square" or tags.get("highway") == "pedestrian":
            ebenen["platz"].append(p)

        h = tags.get("highway")
        if h in STRASSEN_RANG:
            eintrag = {"p": p, "r": STRASSEN_RANG[h]}
            if tags.get("bridge") and "brücke" in name.lower():
                eintrag["n"] = name
            ebenen["strassen"].append(eintrag)
            if tags.get("bridge") and "brücke" in name.lower():
                ebenen["bruecken"].append({"p": p, "n": name})
        elif tags.get("bridge") and "brücke" in name.lower():
            ebenen["bruecken"].append({"p": p, "n": name})

ziel = os.path.join(TMP, "kartenebenen.json")
json.dump(ebenen, open(ziel, "w", encoding="utf-8"),
          ensure_ascii=False, separators=(",", ":"))

for k, v in ebenen.items():
    print(f"  {k:10} {len(v):5d}")
print(f"→ {os.path.getsize(ziel) // 1024} KB")
