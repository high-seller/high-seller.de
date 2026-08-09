#!/usr/bin/env python3
"""Zeichnet die Deutzer Lagekarte aus den ausgelesenen OSM-Ebenen."""
import json
import math
import os

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rohdaten")
AUS = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(TMP, "kartenebenen.json"), encoding="utf-8"))
ZONEN = [z for z in json.load(open(os.path.join(TMP, "boris-deutz.json"), encoding="utf-8"))
         if z["daten"]["ORTST"] == "Deutz" and z["daten"]["ENTW"] == "B"]

B, H = 1040.0, 620.0
LON0, LON1 = 6.9604, 6.9996
LAT0, LAT1 = 50.9334, 50.9472
KOS = math.cos(math.radians((LAT0 + LAT1) / 2))

S = min(B / ((LON1 - LON0) * KOS), H / (LAT1 - LAT0))
OX = (B - (LON1 - LON0) * KOS * S) / 2
OY = (H - (LAT1 - LAT0) * S) / 2


def xy(lon, lat):
    return (OX + (lon - LON0) * KOS * S, OY + (LAT1 - lat) * S)


def vereinfachen(pfad, toleranz=1.0):
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
a('<title id="karte-titel">Lagekarte von Köln-Deutz</title>')
a('<desc id="karte-text">Stadtplan von Köln-Deutz auf Grundlage von '
  'OpenStreetMap-Daten, mit Gebäuden, Straßennetz, Bahntrassen, Grünflächen '
  'und dem Rhein. Der Rhein bildet die westliche Grenze, gequert von '
  'Hohenzollernbrücke und Deutzer Brücke. Eingezeichnet sind zehn Landmarken: '
  'Hyatt Regency und KölnTriangle am Rheinufer, der Bahnhof Köln Messe/Deutz, '
  'die Koelnmesse im Norden, Alt St. Heribert, die Deutzer Freiheit als '
  'Geschäftsstraße, der Von-Sandt-Platz, die Lanxess Arena, die Köln Arcaden '
  'im Osten und die TH Köln am Campus Deutz im Südosten.</desc>')

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
def gross_genug(p, mindest=14.0):
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
rx, ry = xy(LON0 + 0.0014, 50.9430)
a(f'<text x="{rx:.0f}" y="{ry:.0f}" fill="#2C6D9E" font-size="17" '
  f'font-style="italic" transform="rotate(-72 {rx:.0f} {ry:.0f})">Rhein</text>')

# Beide Beschriftungen sitzen ueber dem Wasser, wo sie nichts verdecken.
BRUECKEN = [(6.9632, 50.94185, "Hohenzollernbrücke"),
            (6.9632, 50.93685, "Deutzer Brücke")]
for lon, lat, name in BRUECKEN:
    x, y = xy(lon, lat)
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="11.5" fill="#3D6B92" '
      f'paint-order="stroke" stroke="#BCD6EC" stroke-width="3.5">{name}</text>')

for name, lon, lat in (("Rheinpark", 6.9748, 50.94640),):
    x, y = xy(lon, lat)
    a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12.5" fill="#4F7A4F" '
      f'text-anchor="middle">{name}</text>')

# --- Landmarken -----------------------------------------------------------
FARBE = {"buero": "#2F7CD3", "verkehr": "#0B1A30", "messe": "#8A7434",
         "wohnen": "#2263AE", "bildung": "#3E7D53"}
MARKEN = [
    (6.96959, 50.94038, "Hyatt Regency",
     "Hotel direkt am Rheinufer, am Brückenkopf der Hohenzollernbrücke.",
     "buero", "no"),
    (6.97009, 50.94002, "KölnTriangle",
     "Bürohochhaus am Ottoplatz mit öffentlicher Panoramaetage. Der Blick von dort ist das Motiv, das Deutz bekannt macht.",
     "buero", "sw"),
    (6.97419, 50.94172, "Bahnhof Köln Messe/Deutz",
     "S-Bahn, Regional- und Fernverkehr. Der Hauptgrund, warum Deutz für Pendler und Kapitalanleger interessant ist.",
     "verkehr", "o"),
    (6.98200, 50.94350, "Koelnmesse",
     "Messegelände mit gamescom, ANUGA, ISM und imm cologne. Sorgt ganzjährig für Nachfrage nach möblierter Vermietung.",
     "messe", "o"),
    (6.96965, 50.93795, "Alt St. Heribert",
     "Romanische Kirche am Rheinufer, Wahrzeichen des alten Deutz und Blickpunkt vom Rheinboulevard aus.",
     "wohnen", "w"),
    (6.97136, 50.93690, "Deutzer Freiheit",
     "Die Geschäftsstraße des Stadtteils, von der Deutzer Brücke nach Osten. Nahversorgung, Gastronomie, Stadtbahnhalt.",
     "wohnen", "sw"),
    (6.97680, 50.93840, "Von-Sandt-Platz",
     "Symmetrisch angelegter Platz aus der planmäßigen Erweiterung ab 1907, umgeben von Wohnbebauung der Zwischenkriegszeit.",
     "wohnen", "no"),
    (6.98286, 50.93846, "Lanxess Arena",
     "Veranstaltungshalle mit 20.000 Plätzen, Heimspielstätte der Kölner Haie.",
     "messe", "so"),
    (6.99737, 50.93838, "Köln Arcaden",
     "Einkaufszentrum im Osten des Stadtteils, an der Grenze zu Kalk.",
     "wohnen", "sw"),
    (6.98752, 50.93573, "TH Köln, Campus Deutz",
     "Technische Hochschule mit Fakultäten für Informatik, Maschinenbau und Anlagentechnik. Treiber der Mietnachfrage nach kleinen Wohnungen.",
     "bildung", "so"),
]
VERSATZ = {"o": (15, 4.5, "start"), "w": (-15, 4.5, "end"),
           "no": (15, -10, "start"), "nw": (-15, -10, "end"),
           "so": (15, 19, "start"), "sw": (-15, 19, "end")}

a('<g class="dz-marken">')
for i, (lon, lat, name, text, art, richtung) in enumerate(MARKEN):
    x, y = xy(lon, lat)
    dx, dy, anker = VERSATZ[richtung]
    a(f'<g class="dz-marke" data-nr="{i}" tabindex="0" role="button" aria-label="{name}">'
      f'<circle class="dz-treffer" cx="{x:.1f}" cy="{y:.1f}" r="19" fill="transparent"/>'
      f'<circle class="dz-ring" cx="{x:.1f}" cy="{y:.1f}" r="11.5" fill="none" '
      f'stroke="{FARBE[art]}" stroke-width="2.6"/>'
      f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.8" fill="{FARBE[art]}" '
      f'stroke="#fff" stroke-width="2.4"/>'
      f'<text class="dz-label" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anker}" '
      f'font-size="14" font-weight="600" fill="#12213A" paint-order="stroke" '
      f'stroke="#F7F8F6" stroke-width="4.2" stroke-linejoin="round">{name}</text>'
      f'</g>')
a('</g>')

a(f'<text x="{B - 12:.0f}" y="{H - 10:.0f}" font-size="11" fill="#8B99AA" '
  f'text-anchor="end">Kartendaten: OpenStreetMap-Mitwirkende, ODbL</text>')
a('</svg>')

svg = "\n".join(t)
open(os.path.join(AUS, "karte-deutz.svg"), "w", encoding="utf-8").write(svg)
json.dump({"marken": [{"n": m[2], "t": m[3]} for m in MARKEN],
           "zonen": zonen_info,
           "stufen": [{"f": f, "b": b} for _, f, b in STUFEN]},
          open(os.path.join(AUS, "karte-infos.json"), "w", encoding="utf-8"),
          ensure_ascii=False)
print(f"SVG {len(svg) // 1024} KB")
