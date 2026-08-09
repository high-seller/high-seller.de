#!/usr/bin/env python3
"""Baut die Deutzer Lagekarte aus echten OpenStreetMap-Geodaten.

Die erste Fassung war frei gezeichnet und an mehreren Stellen schlicht falsch:
Die Köln Arcaden lagen mittig statt im Osten, Hyatt und KölnTriangle
untereinander statt nebeneinander, und die Poller Wiesen standen als Deutzer
Grünfläche in der Karte, obwohl sie in Poll liegen.

Hier werden stattdessen die tatsächlichen Umrisse projiziert: Stadtteilgrenze,
Grünflächen, Rheinbrücken und die Landmarken an ihren echten Koordinaten.
Projektion ist eine einfache Plattkarte mit Breitengradkorrektur — bei einer
Ausdehnung von rund vier Kilometern ist der Fehler gegenüber Mercator nicht
sichtbar.
"""
import json
import math
import os

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rohdaten")
AUSGABE = os.path.dirname(os.path.abspath(__file__))
B = 1020.0   # Breite der Zeichenfläche
H = 540.0    # Höhe
RAND = 34.0


def lade(name):
    return json.load(open(os.path.join(TMP, name), encoding="utf-8"))


# --- Stadtteilgrenze zu einem geschlossenen Ring verketten -----------------
def grenzring():
    r = lade("grenze.json")["elements"][0]
    stuecke = [[(p["lon"], p["lat"]) for p in m["geometry"]]
               for m in r["members"]
               if m.get("type") == "way" and "geometry" in m]
    ring = stuecke.pop(0)
    while stuecke:
        beste, bidx, umdrehen = None, None, False
        ende = ring[-1]
        for i, s in enumerate(stuecke):
            for kandidat, dreh in ((s[0], False), (s[-1], True)):
                d = (kandidat[0] - ende[0]) ** 2 + (kandidat[1] - ende[1]) ** 2
                if beste is None or d < beste:
                    beste, bidx, umdrehen = d, i, dreh
        s = stuecke.pop(bidx)
        ring += (s[::-1] if umdrehen else s)[1:]
    return ring


RING = grenzring()
# Fester Ausschnitt auf den bebauten Kern. Die Stadtteilflaeche reicht im Sueden
# weit ueber den Hafen hinaus; zeigte man sie ganz, draengten sich saemtliche
# Landmarken im oberen Fuenftel und die untere Haelfte bliebe leer.
lon0, lon1 = 6.9608, 6.9992
lat0, lat1 = 50.9338, 50.9452
KOS = math.cos(math.radians((lat0 + lat1) / 2))

sx = (B - 2 * RAND) / ((lon1 - lon0) * KOS)
sy = (H - 2 * RAND) / (lat1 - lat0)
S = min(sx, sy)
# zentrieren
ox = RAND + ((B - 2 * RAND) - (lon1 - lon0) * KOS * S) / 2
oy = RAND + ((H - 2 * RAND) - (lat1 - lat0) * S) / 2


def xy(lon, lat):
    return (ox + (lon - lon0) * KOS * S, oy + (lat1 - lat) * S)


def pfad(punkte, zu=True):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in (xy(*p) for p in punkte))
    return d + (" Z" if zu else "")


def wege(datei, filter_fn):
    for e in lade(datei)["elements"]:
        t = e.get("tags", {})
        g = e.get("geometry")
        if g and filter_fn(t):
            yield t, [(p["lon"], p["lat"]) for p in g]


# --- Ebenen ----------------------------------------------------------------
gruen = []
NUR = {"Rheinpark", "Rheingarten", "Von-Sandt-Platz", "Deutzer Stadtgarten",
       "Alter Deutzer Friedhof", "Pyramidenpark"}
for t, g in wege("gruen.json", lambda t: t.get("name") in NUR):
    gruen.append((t["name"], g))

bruecken = {}
for t, g in wege("bruecken.json", lambda t: "brücke" in (t.get("name") or "").lower()):
    n = t["name"]
    if max(p[0] for p in g) - min(p[0] for p in g) > 0.004:
        if n not in bruecken or len(g) > len(bruecken[n]):
            bruecken[n] = g
for t, g in wege("rest.json", lambda t: t.get("name") == "Hohenzollernbrücke"):
    if len(g) >= 2 and (n := "Hohenzollernbrücke") not in bruecken:
        bruecken[n] = g

# Deutzer Freiheit als durchgehende Linie aus den Einzelstücken
df = [g for t, g in wege("rest.json",
                         lambda t: t.get("name") == "Deutzer Freiheit"
                         and t.get("highway") == "residential")]
df_punkte = sorted({p for g in df for p in g})

# --- Landmarken mit echten Koordinaten und Erklärtext ----------------------
# lon, lat, Name, Kurztext für die Infozeile, Art
MARKEN = [
    # lon, lat, Name, Erklärtext, Art, Richtung der Beschriftung
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

FARBE = {"buero": "#2F7CD3", "verkehr": "#0B1A30", "messe": "#8A7434",
         "wohnen": "#2263AE", "bildung": "#3E7D53"}

# --- SVG zusammensetzen ----------------------------------------------------
t = []
a = t.append
a(f'<svg viewBox="0 0 {B:.0f} {H:.0f}" role="img" class="veedelkarte__svg" '
  f'aria-labelledby="karte-titel karte-text">')
a('<title id="karte-titel">Lagekarte von Köln-Deutz</title>')
a('<desc id="karte-text">Karte des Stadtteils Köln-Deutz auf Grundlage von '
  'OpenStreetMap-Daten. Der Rhein bildet die westliche Grenze, gequert von '
  'Hohenzollernbrücke, Deutzer Brücke und Severinsbrücke. Eingezeichnet sind '
  'die Grünflächen, die Deutzer Freiheit als Geschäftsstraße sowie elf '
  'Landmarken von KölnTriangle und Hyatt am Rheinufer über den Bahnhof Köln '
  'Messe/Deutz bis zu Koelnmesse, Lanxess Arena, Köln Arcaden und der TH Köln '
  'am Campus Deutz.</desc>')
a('<defs>'
  '<linearGradient id="dz-rhein" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="#C3DAF0"/><stop offset="1" stop-color="#9AC0E4"/>'
  '</linearGradient>'
  '<linearGradient id="dz-flaeche" x1="0" y1="0" x2="0" y2="1">'
  '<stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#F4F7FA"/>'
  '</linearGradient>'
  '<pattern id="dz-gruen" width="6" height="6" patternTransform="rotate(45)" '
  'patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#E8F1E8"/>'
  '<line x1="0" y1="0" x2="0" y2="6" stroke="#CDE2CD" stroke-width="2"/></pattern>'
  f'<clipPath id="dz-clip"><rect width="{B:.0f}" height="{H:.0f}" rx="2"/></clipPath>'
  '</defs>')

a(f'<rect width="{B:.0f}" height="{H:.0f}" fill="#F7F9FB"/>')
a('<g clip-path="url(#dz-clip)">')

# Rhein: alles westlich der Grenze
westrand = f"M0 0 L{ox:.1f} 0 " + " L".join(
    f"{x:.1f} {y:.1f}" for x, y in (xy(*p) for p in RING)) + f" L{ox:.1f} {H:.0f} L0 {H:.0f} Z"
a(f'<path d="{westrand}" fill="url(#dz-rhein)"/>')

# Stadtteilfläche
a(f'<path d="{pfad(RING)}" fill="url(#dz-flaeche)" stroke="#B9C6D6" '
  f'stroke-width="1.6" stroke-linejoin="round"/>')

# Straßennetz: gibt der Fläche Struktur
for t_, g in wege("strassen.json", lambda t: t.get("highway") in ("primary", "secondary")):
    a(f'<path d="{pfad(g, zu=False)}" fill="none" stroke="#DFE5EC" '
      f'stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>')

# Grünflächen
for name, g in gruen:
    a(f'<path d="{pfad(g)}" fill="url(#dz-gruen)" stroke="#CDE2CD" stroke-width="1"/>')

# Brücken
for name, g in bruecken.items():
    a(f'<path d="{pfad(g, zu=False)}" fill="none" stroke="#94A2B3" '
      f'stroke-width="5" stroke-linecap="round"/>')

# Deutzer Freiheit hervorheben
if df_punkte:
    df_sortiert = sorted(df_punkte)
    a(f'<path d="{pfad(df_sortiert, zu=False)}" fill="none" stroke="#D8C08C" '
      f'stroke-width="6" stroke-linecap="round" opacity=".95"/>')

print(f"Grenze {len(RING)} Punkte | Grün {len(gruen)} | Brücken {len(bruecken)} "
      f"| Deutzer Freiheit {len(df_punkte)} Punkte")

a('</g>')  # Ende des beschnittenen Bereichs

# Beschriftung Rhein und Grünflächen
rx, ry = xy(lon0 + 0.0016, (lat0 + lat1) / 2)
a(f'<text x="{rx:.0f}" y="{ry:.0f}" fill="#2E6A9B" font-size="17" font-style="italic" '
  f'transform="rotate(-90 {rx:.0f} {ry:.0f})" text-anchor="middle">Rhein</text>')
for name in ("Rheinpark",):
    for n, g in gruen:
        if n == name:
            mx = sum(p[0] for p in g) / len(g)
            my = sum(p[1] for p in g) / len(g)
            x, y = xy(mx, my)
            a(f'<text x="{x:.0f}" y="{y:.0f}" font-size="12.5" fill="#4C7A4C" '
              f'text-anchor="middle">{name}</text>')

# Brückennamen
for name, g in bruecken.items():
    if name in ("Deutzer Brücke", "Hohenzollernbrücke", "Severinsbrücke", "Zoobrücke"):
        w = min(g, key=lambda p: p[0])
        x, y = xy(w[0], w[1])
        a(f'<text x="{x + 4:.0f}" y="{y - 7:.0f}" font-size="11.5" fill="#5A6878">{name}</text>')

# Landmarken: anklickbare Gruppen. Die Richtung je Marke ist von Hand gesetzt,
# weil eine automatische Regel bei dieser Dichte immer irgendwo kollidiert.
VERSATZ = {"o": (14, 4.5, "start"), "w": (-14, 4.5, "end"),
           "no": (14, -9, "start"), "nw": (-14, -9, "end"),
           "so": (14, 18, "start"), "sw": (-14, 18, "end")}
a('<g class="dz-marken">')
for i, (lon, lat, name, text, art, richtung) in enumerate(MARKEN):
    x, y = xy(lon, lat)
    dx, dy, anker = VERSATZ[richtung]
    a(f'<g class="dz-marke" data-nr="{i}" tabindex="0" role="button" '
      f'aria-label="{name}">'
      f'<circle class="dz-treffer" cx="{x:.1f}" cy="{y:.1f}" r="19" fill="transparent"/>'
      f'<circle class="dz-ring" cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" '
      f'stroke="{FARBE[art]}" stroke-width="2.4"/>'
      f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{FARBE[art]}" '
      f'stroke="#fff" stroke-width="2.2"/>'
      f'<text class="dz-label" x="{x + dx:.1f}" y="{y + dy:.1f}" text-anchor="{anker}" '
      f'font-size="14" font-weight="600" fill="#12213A" '
      f'paint-order="stroke" stroke="#F7F9FB" stroke-width="4" '
      f'stroke-linejoin="round">{name}</text>'
      f'</g>')
a('</g>')

a(f'<text x="{B - 14:.0f}" y="{H - 12:.0f}" font-size="11" fill="#8B99AA" '
  f'text-anchor="end">Umrisse: OpenStreetMap-Mitwirkende, ODbL</text>')
a('</svg>')

svg = "\n".join(t)
open(os.path.join(AUSGABE, "karte-deutz.svg"), "w", encoding="utf-8").write(svg)

# Infotexte als JSON fürs Skript auf der Seite
infos = [{"n": m[2], "t": m[3]} for m in MARKEN]
open(os.path.join(AUSGABE, "karte-infos.json"), "w", encoding="utf-8").write(
    json.dumps(infos, ensure_ascii=False))
print(f"SVG {len(svg)} Zeichen, {len(MARKEN)} Landmarken")
