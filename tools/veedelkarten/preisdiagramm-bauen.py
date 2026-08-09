#!/usr/bin/env python3
"""Balkendiagramm: Wo steht Deutz im Kölner Preisgefüge?

Form: 20 Stadtteile, ein Messwert, einer davon hervorgehoben. Das ist kein
kategoriales Problem — es braucht zwei Farben, nicht zwanzig. Alle Balken
tragen dieselbe zurückhaltende Farbe, nur Deutz die Markenfarbe. Sortiert nach
Wert, damit die Position ohne Suchen ablesbar ist.

Eine Legende entfällt: Es gibt nur eine Reihe, der Titel benennt sie.
"""
import json
import os

WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TMP = os.path.dirname(os.path.abspath(__file__))

m = json.load(open(os.path.join(WURZEL, "src/data/stadtteile-marktdaten.json")))["stadtteile"]
bez = json.load(open(os.path.join(WURZEL, "src/data/stadtteile-bezirke.json")))["stadtteile"]

zeilen = []
for k, v in m.items():
    if v.get("wv"):
        # Innenstadt liegt in der Zuordnungsdatei nur als Stadtbezirk vor,
        # deshalb der Rückfall auf den großgeschriebenen Schlüssel.
        name = bez.get(k, {}).get("name") or k.capitalize()
        zeilen.append((v["wv"], v.get("wvN", 0), name, k))
zeilen.sort(reverse=True)


# Zwei Farben, nicht zwanzig. Geprueft mit dem Palettenvalidator: Trennung
# Neutral zu Betont ΔE 34,6 bei Protanopie (Schwelle 8), Kontrast zwischen
# beiden 4,23:1. Der Neutralton liegt mit 2,63:1 gegen die Flaeche unter 3:1 —
# das ist bewusst so und zulaessig, weil jeder Balken Name und Wert als
# sichtbares Label traegt und dieselben Zahlen zusaetzlich in der Tabelle
# weiter oben stehen. Die Meldungen des Validators zu Helligkeitsband und
# Farbsaettigung gelten kategorialen Paletten mit gleichrangigen Reihen; hier
# ist die Zuruecknahme der uebrigen Werte gerade der Zweck.
NEUTRAL = "#8AA2BC"
BETONT = "#1E3C64"
INK = "#0C1726"
GEDAEMPFT = "#5F6C85"


def bauen(zeilen, breite, name_b, kennung, fussnote, gekuerzt_nach=None):
    ZH = 27.0
    WERT_B = 92.0
    LINKS = 16.0
    KOPF = 52.0
    H = KOPF + len(zeilen) * ZH + 34

    balken_x = LINKS + name_b
    balken_max = breite - balken_x - WERT_B - LINKS
    hoechst = max(z[0] for z in zeilen)

    t = []
    a = t.append
    a(f'<svg viewBox="0 0 {breite:.0f} {H:.0f}" role="img" '
      f'class="preisdiagramm__svg preisdiagramm__svg--{kennung}" '
      f'aria-labelledby="pd-titel-{kennung} pd-text-{kennung}">')
    a(f'<title id="pd-titel-{kennung}">Kaufpreise für Eigentumswohnungen in '
      f'Kölner Stadtteilen</title>')
    a(f'<desc id="pd-text-{kennung}">Balkendiagramm der durchschnittlichen '
      f'Kaufpreise je Quadratmeter Wohnfläche beim Weiterverkauf von '
      f'Eigentumswohnungen, sortiert vom höchsten zum niedrigsten Wert. '
      f'Köln-Deutz liegt mit 4.690 Euro je Quadratmeter auf Rang 10 von 20 und '
      f'damit genau im Mittelfeld.</desc>')

    a('<g class="pd-raster">')
    for wert in (3000, 4000, 5000, 6000):
        x = balken_x + wert / hoechst * balken_max
        a(f'<line x1="{x:.1f}" y1="{KOPF - 16:.0f}" x2="{x:.1f}" '
          f'y2="{KOPF + len(zeilen) * ZH - 6:.0f}" stroke="#E7EAEF" stroke-width="1"/>')
        a(f'<text x="{x:.1f}" y="{KOPF - 24:.0f}" font-size="11.5" fill="#8B99AA" '
          f'text-anchor="middle">{wert // 1000}.000 €</text>')
    a('</g>')

    for i, (wert, faelle, nm, key) in enumerate(zeilen):
        y = KOPF + i * ZH
        ist_deutz = key == "deutz"
        farbe = BETONT if ist_deutz else NEUTRAL
        breite_b = wert / hoechst * balken_max
        gewicht = "700" if ist_deutz else "400"
        textfarbe = INK if ist_deutz else GEDAEMPFT
        a(f'<g class="pd-zeile">')
        a(f'<text x="{balken_x - 12:.0f}" y="{y + 14:.1f}" text-anchor="end" '
          f'font-size="13.5" font-weight="{gewicht}" fill="{textfarbe}">{nm}</text>')
        a(f'<rect class="pd-balken" x="{balken_x:.1f}" y="{y + 3:.1f}" '
          f'width="{breite_b:.1f}" height="{ZH - 11:.1f}" rx="4" fill="{farbe}"/>')
        a(f'<text class="pd-wert" x="{balken_x + breite_b + 10:.1f}" y="{y + 14:.1f}" '
          f'font-size="13" font-weight="{gewicht}" fill="{textfarbe}">'
          + f'{wert:,}'.replace(",", ".") + ' €</text>')
        a('</g>')
        # Auslassungszeichen, wo Zeilen uebersprungen wurden
        if gekuerzt_nach and i in gekuerzt_nach:
            a(f'<text x="{balken_x - 12:.0f}" y="{y + ZH + 12:.1f}" text-anchor="end" '
              f'font-size="13" fill="#B0BCCA">⋮</text>')

    i_deutz = next(i for i, z in enumerate(zeilen) if z[3] == "deutz")
    y = KOPF + i_deutz * ZH
    a(f'<rect x="{LINKS - 6:.0f}" y="{y - 1:.1f}" width="{breite - 2 * LINKS + 12:.0f}" '
      f'height="{ZH - 5:.1f}" rx="6" fill="none" stroke="{BETONT}" '
      f'stroke-width="1.6" opacity=".45"/>')
    a(f'<text x="{LINKS:.0f}" y="{H - 12:.0f}" font-size="11.5" fill="#8B99AA">'
      f'{fussnote}</text>')
    a('</svg>')
    return "\n".join(t)


QUELLE = ("Mittlere Kaufpreise je m² Wohnfläche, Weiterverkauf von "
          "Eigentumswohnungen. Grundstücksmarktbericht 2026 der Stadt Köln.")

# Volle Fassung: alle zwanzig Stadtteile
voll = bauen(zeilen, 1020.0, 168.0, "breit", QUELLE)

# Fokussierte Fassung fuers Handy: Hoechstwert, die beiden Nachbarn ueber und
# unter Deutz, Deutz selbst und der niedrigste Wert. Sieben Zeilen passen ohne
# seitliches Scrollen; zwanzig taeten es nicht, und abgeschnittene Werte sind
# schlechter als weggelassene.
i_d = next(i for i, z in enumerate(zeilen) if z[3] == "deutz")
auswahl_idx = sorted({0, i_d - 2, i_d - 1, i_d, i_d + 1, i_d + 2, len(zeilen) - 1})
auswahl = [zeilen[i] for i in auswahl_idx]
luecken = {j for j, i in enumerate(auswahl_idx[:-1])
           if auswahl_idx[j + 1] - i > 1}
schmal = bauen(auswahl, 620.0, 132.0, "schmal",
               "Auswahl aus 20 Stadtteilen: Höchstwert, die Nachbarn von Deutz, "
               "niedrigster Wert. Quelle: Grundstücksmarktbericht 2026, Stadt Köln.",
               gekuerzt_nach=luecken)

open(os.path.join(TMP, "diagramm-preise.svg"), "w", encoding="utf-8").write(voll)
open(os.path.join(TMP, "diagramm-preise-schmal.svg"), "w", encoding="utf-8").write(schmal)
print(f"voll: {len(zeilen)} Zeilen, {len(voll)} Zeichen")
print(f"schmal: {len(auswahl)} Zeilen ({[z[2] for z in auswahl]}), {len(schmal)} Zeichen")
print(f"Deutz auf Rang {i_d + 1}")
