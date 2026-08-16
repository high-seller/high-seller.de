#!/usr/bin/env python3
"""Vergibt Abschnitts-IDs und setzt die Sprungleiste auf sechs Veedelseiten.

Die `.jumpbar` gibt es vollständig — sticky, mit Markierung des aktiven
Abschnitts, nur unter 1120 px sichtbar. Sie funktioniert allein durch das
Markup. Auf Raderthal, Raderberg und Marienburg steht sie bereits; die
sechs älteren Seiten konnten sie nicht bekommen, weil ihren `<section>`-
Elementen die `id` fehlt: Deutz und Zollstock hatten gar keine, Sülz eine,
Ehrenfeld und Klettenberg je drei, Lindenthal vier.

Diese Seiten sind zwischen 1.664 und 2.767 Wörter lang und entsprechend
hoch — ohne Navigation heißt das für Leser: scrollen, bis man findet, was
man sucht.

Die IDs sind je Seite von Hand gewählt statt aus den Überschriften
abgeleitet: Automatisch erzeugte Kürzel aus Sätzen wie „Der Höchststand war
2023 — und er ist vorbei" wären lang und unleserlich, und sie sind
dauerhafte Sprungadressen, die auch in Verweisen von außen auftauchen
können.
"""
import os
import re

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Je Seite: Erkennungstext der Überschrift → (ID, Beschriftung in der Leiste).
# Ein leerer Beschriftungstext heißt: ID vergeben, aber nicht in die Leiste.
SEITEN = {
    "deutz": [
        ("Wie Deutz gebaut ist",            "bauweise",     "Bauweise"),
        ("Deutz in Zahlen",                 "zahlen",       "Zahlen"),
        ("Der Höchststand war 2023",        "hoechststand", "Preisverlauf"),
        ("Wer in Deutz kauft",              "kaeufer",      "Käufer"),
        ("Was den Preis Ihrer Deutzer",     "preisfaktoren", ""),
        ("Der Stadtteil, in dem",           "stadtteil",    ""),
        ("So läuft der Verkauf",            "ablauf",       ""),
        ("Sechs Fehler",                    "fehler",       "Fehler"),
        ("Diese Unterlagen brauchen Sie",   "unterlagen",   ""),
        ("Ihre Fragen",                     "fragen",       "Fragen"),
    ],
    "suelz": [
        ("Was diese drei Zahlen",           "zahlen",       "Zahlen"),
        ("Wer in Sülz kauft",               "kaeufer",      "Käufer"),
        ("Zwei Kilometer",                  "preisgefaelle", "Preisgefälle"),
        ("Sülzer Bodenwerte",               "bodenwerte",   "Bodenwerte"),
        ("Wenige hundert Meter",            "mikrolage",    ""),
        ("Der Stadtteil, in dem",           "stadtteil",    ""),
        ("Was vor dem ersten Inserat",      "vorbereitung", "Vorbereitung"),
        ("Ihre Fragen",                     "fragen",       "Fragen"),
    ],
    "zollstock": [
        ("Warum die Zahlen auseinander",    "quellen",      "Preisquellen"),
        ("Zollstock baut",                  "neubau",       "Neubau"),
        ("Sechs Zonen",                     "zonen",        "Bodenzonen"),
        ("Denkmalschutz",                   "denkmal",      "Denkmalschutz"),
        ("Was aus Zollstocker Grundstücken", "grundstuecke", "Grundstücke"),
        ("Das Veedel, in dem",              "veedel",       ""),
        ("Ihre Fragen",                     "fragen",       "Fragen"),
    ],
    "ehrenfeld": [
        ("Warum ausgerechnet Ehrenfeld",    "warum",        "Der Befund"),
        ("Dieselbe Wohnung, zwei Rechnungen", "rechnungen", "Rechenbeispiel"),
        ("Innerhalb Ehrenfelds",            "mikrolage",    "Lagen"),
        ("Nach dem Verkauf",                "danach",       ""),
        ("Häufige Fragen",                  "fragen",       "Fragen"),
    ],
    "lindenthal": [
        ("Warum teurer Boden",              "boden",        "Der Befund"),
        ("Fünf Objektarten",                "objektarten",  "Objektarten"),
        ("Drei Käufergruppen",              "kaeufer",      "Käufer"),
        ("Was Lindenthal von anderen",      "vergleich",    ""),
        ("Wie ein Verkauf in Lindenthal",   "ablauf",       ""),
        ("Häufige Fragen",                  "fragen",       "Fragen"),
    ],
    "klettenberg": [
        ("Zwei Namenswelten",               "namen",        ""),
        ("Denkmalschutz",                   "denkmal",      "Denkmalschutz"),
        ("Warum Unterlagen",                "unterlagen",   "Unterlagen"),
        ("Häufige Fragen",                  "fragen",       "Fragen"),
    ],
}

# Abschnitte, die schon eine ID tragen und mit in die Leiste sollen.
VORHANDEN = {
    "ehrenfeld":   [("preise", "Preise"), ("karte", "Karte"), ("satzung", "Satzung")],
    "lindenthal":  [("bodenanteil", "Bodenanteil"), ("karte", "Karte"), ("preise", "Preise")],
    "klettenberg": [("spreizung", "Der Befund"), ("preise", "Preise"), ("karte", "Karte")],
}

# Reihenfolge in der Leiste je Seite (IDs), höchstens sechs.
LEISTE = {
    "deutz":       ["bauweise", "zahlen", "hoechststand", "kaeufer", "fehler", "fragen"],
    "suelz":       ["zahlen", "kaeufer", "preisgefaelle", "bodenwerte", "vorbereitung", "fragen"],
    "zollstock":   ["quellen", "neubau", "zonen", "denkmal", "grundstuecke", "fragen"],
    "ehrenfeld":   ["warum", "preise", "karte", "satzung", "mikrolage", "fragen"],
    "lindenthal":  ["boden", "bodenanteil", "karte", "preise", "objektarten", "fragen"],
    "klettenberg": ["spreizung", "preise", "karte", "denkmal", "unterlagen", "fragen"],
}


def main():
    os.chdir(WURZEL)
    for kurz, eintraege in SEITEN.items():
        datei = f"immobilienmakler-koeln-{kurz}.html"
        s = open(datei, encoding="utf-8").read()
        if 'id="jumpbar"' in s:
            print(f"{kurz}: Sprungleiste steht bereits")
            continue

        beschriftung = {i: t for _, i, t in eintraege if t}
        for i, t in VORHANDEN.get(kurz, []):
            beschriftung[i] = t
        gesetzt = 0

        for erkennung, kennung, _ in eintraege:
            # Die Section finden, deren erste h2 den Erkennungstext trägt.
            treffer = None
            for m in re.finditer(r'<section([^>]*)>', s):
                rest = s[m.end():m.end() + 2600]
                h2 = re.search(r'<h2[^>]*>(.*?)</h2>', rest, re.S)
                if not h2:
                    continue
                titel = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h2.group(1))).strip()
                if titel.startswith(erkennung) or erkennung in titel:
                    treffer = m
                    break
            if not treffer:
                print(f"  {kurz}: '{erkennung[:34]}' nicht gefunden")
                continue
            if 'id="' in treffer.group(1):
                continue
            s = (s[:treffer.start()] + f'<section{treffer.group(1)} id="{kennung}">'
                 + s[treffer.end():])
            gesetzt += 1

        # Sprungleiste hinter den Kopfbereich setzen.
        ziele = [z for z in LEISTE[kurz] if f'id="{z}"' in s]
        if len(ziele) < 3:
            print(f"  {kurz}: nur {len(ziele)} Ziele vorhanden — übersprungen")
            continue
        leiste = ('<nav class="jumpbar" id="jumpbar" aria-label="Abschnitte dieser Seite">\n'
                  '  <div class="jumpbar__track">\n'
                  + "".join(f'    <a href="#{z}">{beschriftung.get(z, z)}</a>\n' for z in ziele)
                  + '  </div>\n</nav>\n')

        # Nach dem ersten Abschnitt mit id einsetzen — davor liegt der Kopf.
        erste = re.search(r'<section[^>]*id="' + re.escape(ziele[0]) + r'"', s)
        s = s[:erste.start()] + leiste + s[erste.start():]

        open(datei, "w", encoding="utf-8").write(s)
        print(f"{kurz}: {gesetzt} IDs vergeben, Leiste mit {len(ziele)} Zielen")


if __name__ == "__main__":
    main()
