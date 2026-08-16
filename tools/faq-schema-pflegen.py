#!/usr/bin/env python3
"""Bringt das FAQPage-Schema auf den Stand der sichtbaren Fragen.

Auf mehreren Seiten stehen Fragen und Antworten im Text, ohne dass sie im
strukturierten Datensatz auftauchen. Für Leser macht das keinen
Unterschied, für Suchmaschinen schon: Ohne FAQPage-Schema entfällt die
Chance auf erweiterte Suchergebnisse, in denen die Fragen direkt unter dem
Treffer erscheinen.

Gefunden wurden 26 solcher Fragen — Sülz sechs, Ehrenfeld sechs,
Lindenthal neun, Klettenberg vier, Zollstock eine.

Das Werkzeug liest die sichtbaren Fragen in beiden Bauarten, die auf der
Website vorkommen:

  * als `<details class="faq-item">` mit `<summary>` und `.faq-answer`
  * als `<h3>` mit folgendem Absatz innerhalb eines FAQ-Abschnitts

und schreibt sie in den FAQPage-Knoten des letzten JSON-LD-Blocks. Steht
dort noch keiner, wird er angelegt. Umgekehrt wird nichts erfunden: Was
nicht auf der Seite steht, kommt auch nicht ins Schema.

Aufruf:
    python3 tools/faq-schema-pflegen.py            # schreibt
    python3 tools/faq-schema-pflegen.py --pruefen  # meldet nur Abweichungen
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sauber(html):
    """Auszeichnung entfernen, Leerraum vereinheitlichen."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = (text.replace("&middot;", "·").replace("&amp;", "&")
                .replace("&nbsp;", " ").replace("&ndash;", "–")
                .replace("&bdquo;", "„").replace("&ldquo;", "“")
                .replace("&szlig;", "ß").replace("&euro;", "€"))
    return re.sub(r"\s+", " ", text).strip()


def fragen_aus_details(s):
    """Bauart 1: aufklappbare Elemente."""
    aus = []
    for m in re.finditer(r'<details[^>]*>\s*<summary>(.*?)</summary>\s*'
                         r'<div class="faq-answer">(.*?)</div>\s*</details>', s, re.S):
        frage, antwort = sauber(m.group(1)), sauber(m.group(2))
        if frage and antwort and ist_frage(frage):
            aus.append((frage, antwort))
    return aus


def ist_frage(text):
    """Nur echte Fragen gehören ins Schema.

    Diese Prüfung ist der wichtigste Teil des Werkzeugs. Ein erster Anlauf
    ohne sie trug auf 60 Seiten Zwischenüberschriften wie „Was wir
    übernehmen" oder „Makler und Finanzierer in einem" als Fragen ein — für
    Suchmaschinen ist das eine irreführende Auszeichnung und damit
    schlechter als gar keine.
    """
    return text.rstrip().endswith("?")


def fragen_aus_definitionsliste(s):
    """Bauart 2: <dl> mit <dt>/<dd> — so sind die Themenseiten gebaut."""
    aus = []
    for m in re.finditer(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", s, re.S):
        frage, antwort = sauber(m.group(1)), sauber(m.group(2))
        if frage and antwort and ist_frage(frage):
            aus.append((frage, antwort))
    return aus


def fragen_aus_ueberschriften(s):
    """Bauart 3: <h3> mit Folgeabsätzen im FAQ-Abschnitt.

    Der Abschnitt wird über seine Überschrift erkannt („Ihre Fragen" oder
    „Häufige Fragen"). Zusätzlich muss jede Überschrift eine echte Frage
    sein — in denselben Abschnitten stehen auch Zwischenüberschriften.
    """
    m = re.search(r'<h2[^>]*>[^<]*(?:Ihre Fragen|Häufige Fragen)[^<]*</h2>(.*?)</section>',
                  s, re.S)
    if not m:
        return []
    block = m.group(1)
    aus = []
    teile = re.split(r"<h3[^>]*>", block)[1:]
    for teil in teile:
        ende = teil.find("</h3>")
        if ende < 0:
            continue
        frage = sauber(teil[:ende])
        if not ist_frage(frage):
            continue
        rest = teil[ende + 5:]
        # Alle Absätze bis zur nächsten Überschrift gehören zur Antwort.
        absaetze = re.findall(r"<p[^>]*>(.*?)</p>", rest.split("<h2")[0], re.S)
        antwort = " ".join(sauber(a) for a in absaetze).strip()
        if antwort:
            aus.append((frage, antwort))
    return aus


def schema_fragen(s):
    """Vorhandene Fragen im FAQPage-Knoten, samt Fundstelle.

    Falls eine Seite mehrere FAQPage-Auszeichnungen trägt, wird die mit den
    meisten Fragen zurückgegeben — und die Doppelung gemeldet. Zwei
    FAQPage-Knoten auf einer Seite sind kein doppelter Nutzen, sondern ein
    Fehler: Für Suchmaschinen ist dann nicht bestimmt, welche gilt. Das ist
    beim Ausbau der Marienburg-Seite einmal passiert, weil ein bereits
    vorhandener eigenständiger Block übersehen wurde.
    """
    treffer = []
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        for node in (d.get("@graph") or [d]):
            if node.get("@type") == "FAQPage":
                treffer.append(([q.get("name", "") for q in node.get("mainEntity", [])], m))
    if len(treffer) > 1:
        print(f"     ACHTUNG: {len(treffer)} FAQPage-Knoten auf dieser Seite — "
              f"vor dem Schreiben zusammenführen")
    if not treffer:
        return [], None
    return max(treffer, key=lambda t: len(t[0]))


def main():
    nur_pruefen = "--pruefen" in sys.argv
    os.chdir(WURZEL)
    geaendert = stimmig = ohne_faq = 0

    for datei in sorted(os.listdir(".")):
        if not datei.endswith(".html") or datei.startswith("__"):
            continue
        s = open(datei, encoding="utf-8").read()

        sichtbar = (fragen_aus_details(s) or fragen_aus_definitionsliste(s)
                    or fragen_aus_ueberschriften(s))
        if not sichtbar:
            ohne_faq += 1
            continue

        vorhanden, block = schema_fragen(s)
        if [f for f, _ in sichtbar] == vorhanden:
            stimmig += 1
            continue

        print(f"  {datei[:48]:48} {len(vorhanden)} → {len(sichtbar)} Fragen")
        if nur_pruefen:
            geaendert += 1
            continue

        eintraege = [{"@type": "Question", "name": f,
                      "acceptedAnswer": {"@type": "Answer", "text": a}}
                     for f, a in sichtbar]

        if block:
            d = json.loads(block.group(1))
            knoten = d.get("@graph") or [d]
            for node in knoten:
                if node.get("@type") == "FAQPage":
                    node["mainEntity"] = eintraege
                    break
            neu = json.dumps(d, ensure_ascii=False, indent=2)
            s = s[:block.start(1)] + neu + s[block.end(1):]
        else:
            # Kein FAQPage vorhanden: in den letzten Graph-Block aufnehmen.
            bloecke = list(re.finditer(
                r'<script type="application/ld\+json">(.*?)</script>', s, re.S))
            if not bloecke:
                print(f"     übersprungen — kein JSON-LD-Block")
                continue
            ziel = bloecke[-1]
            d = json.loads(ziel.group(1))
            if "@graph" not in d:
                d = {"@context": "https://schema.org", "@graph": [d]}
            d["@graph"].append({
                "@type": "FAQPage",
                "@id": f"https://high-seller.de/{datei}#faq",
                "mainEntity": eintraege})
            neu = json.dumps(d, ensure_ascii=False, indent=2)
            s = s[:ziel.start(1)] + neu + s[ziel.end(1):]

        open(datei, "w", encoding="utf-8").write(s)
        geaendert += 1

    wort = "Abweichung(en)" if nur_pruefen else "Seite(n) aktualisiert"
    print(f"\n{geaendert} {wort}   bereits stimmig: {stimmig}   ohne FAQ: {ohne_faq}")


if __name__ == "__main__":
    main()
