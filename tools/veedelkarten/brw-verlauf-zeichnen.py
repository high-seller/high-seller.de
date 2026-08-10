#!/usr/bin/env python3
"""Zeichnet den Bodenrichtwert-Verlauf als Liniendiagramm.

Eine Reihe, deshalb keine Legende — der Titel benennt sie. Der Höchststand
2023 und der aktuelle Wert sind direkt beschriftet, die Zwischenjahre nicht:
eine Zahl an jedem Punkt macht die Kurve unlesbar.
"""
import json
import os
import statistics

TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rohdaten")
AUS = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(TMP, "brw-verlauf.json"), encoding="utf-8"))
JAHRE = [2011, 2015, 2019, 2023, 2024, 2025, 2026]

B, H = 720.0, 340.0
L, R, O, U = 62.0, 96.0, 50.0, 44.0

LINIE = "#1E3C64"
FLAECHE = "#DCE7F3"
GITTER = "#E7EAEF"
TINTE = "#0C1726"
GEDAEMPFT = "#5F6C85"
WARN = "#A8452F"


def reihe(stadtteil):
    zonen = [v["reihe"] for v in D[stadtteil].values() if v["nutzung"] in ("WA", "WB")]
    aus = []
    for j in JAHRE:
        w = [r[str(j)] for r in zonen if str(j) in r]
        aus.append(statistics.median(w) if w else None)
    return aus


def bauen(stadtteil, name):
    werte = reihe(stadtteil)
    gueltig = [w for w in werte if w]
    hoch = max(gueltig)
    obergrenze = (int(hoch / 250) + 1) * 250

    def x(i):
        return L + (B - L - R) * i / (len(JAHRE) - 1)

    def y(w):
        return H - U - (H - U - O) * (w / obergrenze)

    t = []
    a = t.append
    a(f'<svg viewBox="0 0 {B:.0f} {H:.0f}" role="img" class="verlauf__svg" '
      f'aria-labelledby="vl-t-{stadtteil} vl-d-{stadtteil}">')
    a(f'<title id="vl-t-{stadtteil}">Bodenrichtwerte in {name} von 2011 bis 2026</title>')
    beschreibung = ", ".join(
        f"{j}: {int(w)} Euro" for j, w in zip(JAHRE, werte) if w)
    a(f'<desc id="vl-d-{stadtteil}">Liniendiagramm des mittleren Bodenrichtwerts '
      f'der Wohnbauzonen in {name}, je Quadratmeter Grundstücksfläche. {beschreibung}. '
      f'Der Höchststand lag 2023, danach fielen die Werte um rund ein Fünftel und '
      f'liegen seit 2025 stabil.</desc>')

    # Gitter und Achsenbeschriftung
    a('<g class="vl-gitter">')
    schritt = 500 if obergrenze > 1500 else 250
    w = 0
    while w <= obergrenze:
        yy = y(w)
        a(f'<line x1="{L:.0f}" y1="{yy:.1f}" x2="{B-R:.0f}" y2="{yy:.1f}" '
          f'stroke="{GITTER}" stroke-width="1"/>')
        a(f'<text x="{L-10:.0f}" y="{yy+4:.1f}" font-size="12" fill="{GEDAEMPFT}" '
          f'text-anchor="end">{w:,}'.replace(",", ".") + '</text>')
        w += schritt
    a('</g>')
    for i, j in enumerate(JAHRE):
        a(f'<text x="{x(i):.1f}" y="{H-U+22:.0f}" font-size="12" fill="{GEDAEMPFT}" '
          f'text-anchor="middle">{j}</text>')

    punkte = [(x(i), y(w)) for i, w in enumerate(werte) if w]

    # Fläche unter der Kurve
    flaeche = ("M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in punkte)
               + f" L{punkte[-1][0]:.1f} {H-U:.1f} L{punkte[0][0]:.1f} {H-U:.1f} Z")
    a(f'<path d="{flaeche}" fill="{FLAECHE}" opacity=".75"/>')

    # Kurve
    linie = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in punkte)
    a(f'<path class="vl-linie" d="{linie}" fill="none" stroke="{LINIE}" '
      f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')

    # Punkte
    for i, wert in enumerate(werte):
        if not wert:
            continue
        hoehepunkt = wert == hoch
        a(f'<circle cx="{x(i):.1f}" cy="{y(wert):.1f}" r="{5.2 if hoehepunkt else 3.8}" '
          f'fill="{WARN if hoehepunkt else LINIE}" stroke="#fff" stroke-width="2"/>')

    # Nur Höchststand und aktueller Wert beschriften
    i_hoch = werte.index(hoch)
    a(f'<text x="{x(i_hoch):.1f}" y="{y(hoch)-16:.1f}" font-size="14" font-weight="700" '
      f'fill="{WARN}" text-anchor="middle">{int(hoch):,} €'.replace(",", ".") + '</text>')
    a(f'<text x="{x(i_hoch):.1f}" y="{y(hoch)-32:.1f}" font-size="11.5" '
      f'fill="{WARN}" text-anchor="middle">Höchststand</text>')

    letzt = werte[-1]
    a(f'<text x="{B-R+12:.0f}" y="{y(letzt)+1:.1f}" font-size="15" font-weight="700" '
      f'fill="{TINTE}">{int(letzt):,} €'.replace(",", ".") + '</text>')
    a(f'<text x="{B-R+12:.0f}" y="{y(letzt)+18:.1f}" font-size="11.5" '
      f'fill="{GEDAEMPFT}">je m² heute</text>')

    a(f'<text x="{L-10:.0f}" y="{O-12:.0f}" font-size="11.5" fill="{GEDAEMPFT}" '
      f'text-anchor="end">€/m²</text>')
    a('</svg>')

    return "\n".join(t), werte


aus = {}
for st, name in (("deutz", "Köln-Deutz"), ("suelz", "Köln-Sülz")):
    svg, werte = bauen(st, name)
    aus[st] = {"svg": svg, "werte": {str(j): w for j, w in zip(JAHRE, werte)}}
    hoch = max(w for w in werte if w)
    print(f"{name}: 2011 {int(werte[0])} → Höchst {int(hoch)} → heute {int(werte[-1])} "
          f"({(werte[-1]/hoch-1)*100:+.0f} % gegenüber Höchststand, "
          f"{werte[-1]/werte[0]:.1f}x gegenüber 2011), SVG {len(svg)} Zeichen")

json.dump(aus, open(os.path.join(AUS, "verlauf-diagramme.json"), "w", encoding="utf-8"),
          ensure_ascii=False)
