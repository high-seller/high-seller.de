#!/usr/bin/env python3
"""Zeichnet die Deutzer Lagekarte aus den ausgelesenen OSM-Ebenen."""
import json
import math
import os

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rohdaten")
AUS = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(TMP, "kartenebenen-zolli.json"), encoding="utf-8"))
ZONEN = [z for z in json.load(open(os.path.join(TMP, "boris-zollstock.json"), encoding="utf-8"))
         if z["daten"]["ORTST"] == "Zollstock" and z["daten"]["ENTW"] == "B"]

B, H = 1040.0, 900.0
LON0, LON1 = 6.9240, 6.9540
LAT0, LAT1 = 50.8955, 50.9215
KOS = math.cos(math.radians((LAT0 + LAT1) / 2))

S = min(B / ((LON1 - LON0) * KOS), H / (LAT1 - LAT0))
OX = (B - (LON1 - LON0) * KOS * S) / 2
OY = (H - (LAT1 - LAT0) * S) / 2


def xy(lon, lat):
    return (OX + (lon - LON0) * KOS * S, OY + (LAT1 - lat) * S)


def vereinfachen(pfad, toleranz=1.2):
    """Douglas-Peucker. Ohne diesen Schritt wiegt die Karte ueber 500 KB, weil
    1.600 Gebaeudeumrisse jede Hausecke einzeln mitbringen."""
    if len(pfad) < 3:
        return pfad
    ax, ay = pfad[0]
    bx, by = pfad[-1]
    dx, dy = bx - ax, by - ay
    laenge = math.hypot(dx, dy)
    weit, idx = 0.0, 0
    for i in range(1, len(pfad) - 1):
        px, py = pfad[i]
        if laenge < 1e-9:
            abstand = math.hypot(px - ax, py - ay)
        else:
            abstand = abs(dy * px - dx * py + bx * ay - by * ax) / laenge
        if abstand > weit:
            weit, idx = abstand, i
    if weit <= toleranz:
        return [pfad[0], pfad[-1]]
    return (vereinfachen(pfad[:idx + 1], toleranz)[:-1]
            + vereinfachen(pfad[idx:], toleranz))


def d(punkte, zu=False):
    roh = [xy(*p) for p in punkte]
    fein = vereinfachen(roh)
    aus, vorher = [], None
    for x, y in fein:
        q = (round(x), round(y))
        if q != vorher:
            aus.append(q)
            vorher = q
    if len(aus) < 2:
        aus = [(round(x), round(y)) for x, y in roh[:2]] or [(0, 0), (0, 0)]
    s = "M" + " L".join(f"{x} {y}" for x, y in aus)
    return s + (" Z" if zu else "")


def sichtbar(punkte, rand=0.0012):
    return any(LON0 - rand <= x <= LON1 + rand and LAT0 - rand <= y <= LAT1 + rand
               for x, y in punkte)


t = []
a = t.append
a(f'<svg viewBox="0 0 {B:.0f} {H:.0f}" role="img" class="veedelkarte__svg" '
  f'aria-labelledby="karte-titel karte-text">')
a('<title id="karte-titel">Lagekarte von Köln-Zollstock</title>')
a('<desc id="karte-text">Stadtplan von Köln-Zollstock auf Grundlage von '
  'OpenStreetMap-Daten, mit Gebäuden, Straßennetz und Grünflächen. '
  'Eingezeichnet sind sechs Orientierungspunkte: das Südstadion des SC Fortuna '
  'Köln, der Höninger Weg als Hauptachse, die Zollstock-Arkaden als '
  'Nahversorgung, der Vorgebirgspark als Grünfläche, die Stadtbahnlinie 12 und '
  'das Zollstockbad. In der zweiten Ansicht liegen die sechs amtlichen '
  'Bodenrichtwertzonen darüber.</desc>')

a('<defs>'
  '<linearGradient id="dz-w" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#BCD6EC"/><stop offset="1" stop-color="#9FC2E0"/>'
  '</linearGradient>'
  f'<clipPath id="dz-clip"><rect width="{B:.0f}" height="{H:.0f}"/></clipPath>'
  '</defs>')

a(f'<rect width="{B:.0f}" height="{H:.0f}" fill="#F2F4F1"/>')
a('<g clip-path="url(#dz-clip)">')

# --- Wasser ---------------------------------------------------------------
# Der Rhein liegt als Aussenring einer Relation vor. Alles westlich davon ist
# Wasser; die Flaeche wird bis zum linken Rand aufgefuellt.
for p in E["ufer"]:
    a(f'<path d="{d(p, zu=True)}" fill="url(#dz-w)"/>')
for p in E["wasser"]:
    a(f'<path d="{d(p, zu=True)}" fill="url(#dz-w)"/>')

# --- Grün -----------------------------------------------------------------
for g in E["gruen"]:
    if sichtbar(g["p"]):
        a(f'<path d="{d(g["p"], zu=True)}" fill="#DCE8D6"/>')

# --- Gebäude --------------------------------------------------------------
# Die eigentliche Wiedererkennung. Ohne sie wirkt die Flaeche wie ein leerer
# Umriss; mit ihnen liest man auf den ersten Blick einen Stadtplan.
def gross_genug(p, mindest=18.0):
    xs = [q[0] for q in p]; ys = [q[1] for q in p]
    (x0, y0), (x1, y1) = xy(min(xs), max(ys)), xy(max(xs), min(ys))
    return (x1 - x0) * (y1 - y0) >= mindest


gebaeude = [p for p in E["gebaeude"] if sichtbar(p) and gross_genug(p)]
a('<g fill="#E2E0DC" stroke="#D2CFC9" stroke-width="0.4">')
for p in gebaeude:
    a(f'<path d="{d(p, zu=True)}"/>')
a('</g>')

# --- Straßen: erst breite helle Unterlage, dann die Fahrbahn --------------
RANG = {1: (7.0, "#F4CDA0"), 2: (5.6, "#F8DFB4"), 3: (4.4, "#FBF3D4"),
        4: (3.4, "#FFFFFF"), 5: (2.4, "#FFFFFF")}
strassen = [s for s in E["strassen"] if sichtbar(s["p"])]
for rang in (5, 4, 3, 2, 1):
    breite, farbe = RANG[rang]
    a(f'<g fill="none" stroke="#DFDCD6" stroke-width="{breite + 1.4:.1f}" '
      f'stroke-linecap="round" stroke-linejoin="round">')
    for s in strassen:
        if s["r"] == rang:
            a(f'<path d="{d(s["p"])}"/>')
    a('</g>')
    a(f'<g fill="none" stroke="{farbe}" stroke-width="{breite:.1f}" '
      f'stroke-linecap="round" stroke-linejoin="round">')
    for s in strassen:
        if s["r"] == rang:
            a(f'<path d="{d(s["p"])}"/>')
    a('</g>')

# --- Bahn: der markante Bogen durch Deutz --------------------------------
bahn = [p for p in E["bahn"] if sichtbar(p)]
a('<g fill="none" stroke="#B4BCC6" stroke-width="2.6" stroke-linecap="round">')
for p in bahn:
    a(f'<path d="{d(p)}"/>')
a('</g>')
a('<g fill="none" stroke="#FFFFFF" stroke-width="1.1" stroke-dasharray="5 5">')
for p in bahn:
    a(f'<path d="{d(p)}"/>')
a('</g>')

# --- Bodenrichtwertzonen -------------------------------------------------
# Die zweite Ansicht der Karte. Amtliche Zonen aus BORIS NRW, Stichtag
# 1.1.2026. Gestuft statt stufenlos eingefaerbt: Die Spanne reicht von 175 bis
# 4.000 Euro je Quadratmeter, eine lineare Skala liesse alle Wohnlagen gleich
# aussehen.
NUTZUNG = {"WB": "Besonderes Wohngebiet", "WA": "Allgemeines Wohngebiet",
           "WR": "Reines Wohngebiet", "MI": "Mischgebiet", "MK": "Kerngebiet",
           "SO": "Sondergebiet", "GE": "Gewerbegebiet"}
STUFEN = [(1000, "#E4EEF8", "unter 1.000 €"), (1500, "#BBD7EF", "1.000–1.500 €"),
          (2500, "#87B3DD", "1.500–2.500 €"), (3500, "#4E86C4", "2.500–3.500 €"),
          (10**9, "#255F9E", "über 3.500 €")]


def stufe(wert):
    for grenze, farbe, _ in STUFEN:
        if wert < grenze:
            return farbe
    return STUFEN[-1][1]


zonen_info = []
a('<g class="dz-zonen">')
for i, z in enumerate(sorted(ZONEN, key=lambda x: -int(x["daten"]["BRW"]))):
    dat = z["daten"]
    wert = int(dat["BRW"])
    # .get statt [], weil im eingedampften Auszug leere Felder ganz fehlen
    bem = dat.get("BEM", "")
    gfz = dat.get("GFZ", "")
    pfade = " ".join(d(r, zu=True) for r in z["ringe"])
    a(f'<g class="dz-zone" data-zone="{i}" tabindex="0" role="button" '
      f'aria-label="Bodenrichtwertzone {bem or dat["BRWZNR"]}, {wert} Euro je Quadratmeter">'
      f'<path d="{pfade}" fill="{stufe(wert)}" fill-opacity=".72" '
      f'stroke="#2A5F92" stroke-width="1.1" stroke-opacity=".55"/></g>')
    xs = [p[0] for r in z["ringe"] for p in r]
    ys = [p[1] for r in z["ringe"] for p in r]
    mx, my = xy(sum(xs) / len(xs), sum(ys) / len(ys))
    # Nur groessere Zonen beschriften, sonst ueberlagern sich die Zahlen.
    if len(xs) > 40:
        a(f'<text class="dz-zonenwert" x="{mx:.0f}" y="{my:.0f}" text-anchor="middle" '
          f'font-size="13" font-weight="700" fill="#0C1726" paint-order="stroke" '
          f'stroke="#fff" stroke-width="3.4">{wert:,}'.replace(",", ".") + ' €</text>')
    zonen_info.append({
        "n": f"{wert:,}".replace(",", ".") + " € je m²",
        "t": (f"{NUTZUNG.get(dat['NUTA'], dat['NUTA'])}"
              + (f", Lage {bem}" if bem else "")
              + (f", Geschossflächenzahl {gfz}" if gfz else "")
              + f". Amtlicher Bodenrichtwert zum Stichtag 1.1.2026, Zone {dat['BRWZNR']}."),
    })
a('</g>')

a('</g>')

print(f"Zonen {len(ZONEN)}, Gebäude {len(gebaeude)}, Straßen {len(strassen)}, "
      f"Bahn {len(bahn)}")

# --- Beschriftung ---------------------------------------------------------


for name, lon, lat in (("Vorgebirgspark", 6.9515, 50.9098),):
    x, y = xy(lon, lat)
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12.5" fill="#4F7A4F" '
      f'text-anchor="middle">{name}</text>')

# --- Landmarken -----------------------------------------------------------
FARBE = {"wohnen": "#2263AE", "gruen": "#3E7D53", "freizeit": "#B4553A",
         "verkehr": "#0B1A30"}
MARKEN = [
    # Koordinaten aus Nominatim, nicht geschätzt.
    (6.94354, 50.91738, "Südstadion",
     "Heimat des SC Fortuna Köln, dazu Sportplätze und ein regelmäßiger Flohmarkt. Der Bezugspunkt, den viele Kölner mit Zollstock verbinden.",
     "freizeit", "o"),
    (6.94210, 50.91290, "Höninger Weg",
     "Die Hauptachse des Veedels: Lebensmittel, Bäckereien, Apotheken, Gastronomie und donnerstags der Wochenmarkt an der Herthastraße.",
     "wohnen", "w"),
    (6.94529, 50.91313, "Zollstock-Arkaden",
     "Nahversorgung gebündelt an der Vorgebirgstraße, dazu Ärzte und Dienstleistungen. Für Käufer ein konkreter Alltagsvorteil.",
     "wohnen", "o"),
    (6.95092, 50.91060, "Vorgebirgspark",
     "Die große Grünfläche des Stadtteils. Für Familien, Hundebesitzer und sportlich Aktive das stärkste Lageargument.",
     "gruen", "o"),
    (6.94113, 50.91711, "Stadtbahn 12",
     "Haltestellen Zollstockgürtel, Gottesweg und Pohligstraße verbinden das Veedel mit Südstadt und Innenstadt.",
     "verkehr", "sw"),
    (6.94861, 50.90487, "Zollstockbad",
     "Hallen- und Freibad am Raderthalgürtel, unmittelbar südlich des Stadtteils.",
     "freizeit", "so"),
]
VERSATZ = {"o": (15, 4.5, "start"), "w": (-15, 4.5, "end"),
           "no": (15, -10, "start"), "nw": (-15, -10, "end"),
           "so": (15, 19, "start"), "sw": (-15, 19, "end")}

a('<g class="dz-marken">')
for i, (lon, lat, name, text, art, richtung) in enumerate(MARKEN):
    x, y = xy(lon, lat)
    # Ziffer statt Name: Bei voller Skalierung auf Telefonbreite
    # schrumpft ein Straßenname auf knapp fünf Pixel. Die Namen stehen
    # als Liste unter der Karte. Die sichtbare Ziffer gehört in das
    # aria-label, sonst findet die Sprachsteuerung den Punkt nicht.
    a(f'<g class="dz-marke" data-nr="{i}" tabindex="0" role="button" '
      f'aria-label="{i + 1}. {name}">'
      f'<circle class="dz-treffer" cx="{x:.1f}" cy="{y:.1f}" fill="transparent"/>'
      f'<circle class="dz-ring" cx="{x:.1f}" cy="{y:.1f}" fill="{FARBE[art]}" '
      f'stroke="#fff" stroke-width="3"/>'
      f'<text class="dz-nr" x="{x:.1f}" y="{y:.1f}" text-anchor="middle" '
      f'dominant-baseline="central" font-weight="700" fill="#fff">{i + 1}</text>'
      f'</g>')
a('</g>')

a(f'<text x="{B - 12:.0f}" y="{H - 10:.0f}" font-size="11" fill="#8B99AA" '
  f'text-anchor="end">Kartendaten: OpenStreetMap-Mitwirkende, ODbL</text>')
a('</svg>')

svg = "\n".join(t)
open(os.path.join(AUS, "karte-zolli.svg"), "w", encoding="utf-8").write(svg)
json.dump({"marken": [{"n": m[2], "t": m[3]} for m in MARKEN],
           "zonen": zonen_info,
           "stufen": [{"f": f, "b": b} for _, f, b in STUFEN]},
          open(os.path.join(AUS, "karte-infos-zolli.json"), "w", encoding="utf-8"),
          ensure_ascii=False)
print(f"SVG {len(svg) // 1024} KB")
