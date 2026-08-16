#!/usr/bin/env python3
"""Nimmt alle ausgebauten Stadtteilseiten in die Fußzeile auf.

Bisher standen dort vier feste Verweise — Köln, Lindenthal, Sülz und
Ehrenfeld — plus ein Verweis auf die Seite selbst. Das erklärt einen
auffälligen Unterschied in der internen Verlinkung: Lindenthal, Sülz und
Ehrenfeld werden von 230 Seiten verlinkt, Deutz dagegen von 14, Zollstock
von 16, Klettenberg von 17 und Raderthal von 11.

Interne Links sind das Mittel, mit dem eine Seite Gewicht innerhalb der
eigenen Domain bekommt. Dass ausgerechnet die aufwendig ausgebauten Seiten
kaum verlinkt sind, während 55 dünne Umlandseiten dieselbe Behandlung
erfahren, ist genau verkehrt herum.

Die feste Liste enthält deshalb künftig alle Seiten, die inhaltlich
ausgebaut sind. Der Selbstverweis bleibt erhalten, erscheint aber nicht
doppelt, wenn die Seite ohnehin schon in der Liste steht.
"""
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Reihenfolge wie die Überarbeitung: Die Übersicht zuerst, dann die
# ausgebauten Veedel, zuletzt Rodenkirchen als Bezirksseite.
FEST = [
    ("immobilienmakler-koeln.html", "Immobilienmakler Köln"),
    ("immobilienmakler-koeln-deutz.html", "Köln Deutz"),
    ("immobilienmakler-koeln-suelz.html", "Köln Sülz"),
    ("immobilienmakler-koeln-zollstock.html", "Köln Zollstock"),
    ("immobilienmakler-koeln-ehrenfeld.html", "Köln Ehrenfeld"),
    ("immobilienmakler-koeln-lindenthal.html", "Köln Lindenthal"),
    ("immobilienmakler-koeln-klettenberg.html", "Köln Klettenberg"),
    ("immobilienmakler-koeln-raderthal.html", "Köln Raderthal"),
    ("immobilienmakler-koeln-raderberg.html", "Köln Raderberg"),
    ("immobilienmakler-koeln-rodenkirchen.html", "Köln Rodenkirchen"),
]
FESTE_DATEIEN = {d for d, _ in FEST}

BLOCK = re.compile(
    r'(<div class="footcol"><h4>Standorte Köln</h4><ul>)(.*?)(</ul></div>)', re.S)
LINK = re.compile(r'<li><a href="([^"]+)">([^<]+)</a></li>')


def main():
    os.chdir(WURZEL)
    geaendert = unveraendert = ohne = 0

    for datei in sorted(os.listdir(".")):
        if not datei.endswith(".html"):
            continue
        s = open(datei, encoding="utf-8").read()
        m = BLOCK.search(s)
        if not m:
            ohne += 1
            continue

        # Der Selbstverweis der Seite bleibt, sofern sie nicht ohnehin in der
        # festen Liste steht.
        vorhanden = LINK.findall(m.group(2))
        eigen = [(z, t) for z, t in vorhanden
                 if z == datei and datei not in FESTE_DATEIEN]

        posten = list(FEST) + eigen
        neu_inhalt = "\n      " + "\n      ".join(
            f'<li><a href="{z}">{t}</a></li>' for z, t in posten) + "\n    "

        if neu_inhalt == m.group(2):
            unveraendert += 1
            continue

        s = s[:m.start(2)] + neu_inhalt + s[m.end(2):]
        open(datei, "w", encoding="utf-8").write(s)
        geaendert += 1

    print(f"Fußzeile angepasst auf {geaendert} Seiten")
    print(f"  bereits richtig: {unveraendert}   ohne Standortblock: {ohne}")


if __name__ == "__main__":
    main()
