#!/usr/bin/env python3
"""Hält die Sitemap für überarbeitete Seiten aktuell.

Warum das ein eigenes Werkzeug braucht: Die Sitemap ist an zwei Stellen
wirksam, und beide gehen still kaputt, wenn sie nicht gepflegt wird.

1. **Suchmaschinen.** Ein `lastmod`, das älter ist als die Überarbeitung,
   sagt Google, an der Seite habe sich nichts geändert. Eine von 600 auf
   2.400 Wörter ausgebaute Seite wird dann unter Umständen monatelang in
   der alten Fassung ausgeliefert.
2. **Die sichtbare Autorzeile.** `tools/autorschaft-pflegen.py` liest das
   Datum *aus dieser Datei* und schreibt es als „zuletzt geprüft am" auf
   jede Seite. Ein veraltetes `lastmod` erzeugt dort also eine falsche
   Angabe gegenüber dem Leser.

Genau das war der Fall: Ehrenfeld, Lindenthal und Klettenberg standen nach
ihrer Überarbeitung noch auf dem 28. Juli beziehungsweise 31. Juli.

Aufruf:
    python3 tools/sitemap-pflegen.py                # setzt die Tabelle unten
    python3 tools/sitemap-pflegen.py --pruefen      # meldet nur Abweichungen
"""
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(WURZEL, "sitemap.xml")

# Stand der inhaltlichen Überarbeitung je Seite. Das Datum des letzten
# Commits taugt dafür nicht: Ein Cache-Buster-Lauf fasst alle 231 Dateien an,
# ohne dass sich an einer davon der Inhalt geändert hätte.
UEBERARBEITET = {
    "immobilienmakler-koeln-deutz.html":       ("2026-08-09", "0.8"),
    "immobilienmakler-koeln-suelz.html":       ("2026-08-10", "0.8"),
    "immobilienmakler-koeln-zollstock.html":   ("2026-08-11", "0.8"),
    "immobilienmakler-koeln-ehrenfeld.html":   ("2026-08-13", "0.8"),
    "immobilienmakler-koeln-lindenthal.html":  ("2026-08-14", "0.8"),
    "immobilienmakler-koeln-klettenberg.html": ("2026-08-15", "0.8"),
    "immobilienmakler-koeln-raderthal.html":   ("2026-08-16", "0.8"),
    "immobilienmakler-koeln-raderberg.html":   ("2026-08-16", "0.8"),
    "immobilienmakler-koeln-marienburg.html":  ("2026-08-16", "0.8"),
    "immobilienmakler-koeln-hahnwald.html":    ("2026-08-16", "0.8"),
    "immobilienmarktbericht-koeln-2026.html":  ("2026-08-16", "0.9"),
}

# Ausgebaute Seiten erscheinen häufiger in den Ergebnissen, wenn sie nicht
# mit den 167 Standardseiten auf derselben Stufe stehen. 0.8 hebt sie über
# das Feld, ohne mit der Startseite (1.0) zu konkurrieren.


def eintraege(roh):
    """Alle <url>-Blöcke mit ihrem Dateinamen."""
    for m in re.finditer(r"<url>(.*?)</url>", roh, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", m.group(1))
        if not loc:
            continue
        letzt = loc.group(1).rstrip("/").split("/")[-1]
        name = letzt if letzt.endswith(".html") else "index.html"
        yield name, m


def main():
    nur_pruefen = "--pruefen" in sys.argv
    roh = open(SITEMAP, encoding="utf-8").read()

    gefunden = {name: m for name, m in eintraege(roh)}
    fehlend = [s for s in UEBERARBEITET if s not in gefunden]
    for s in fehlend:
        print(f"  FEHLT in der Sitemap: {s}")

    aenderungen = []
    for seite, (datum, prio) in UEBERARBEITET.items():
        m = gefunden.get(seite)
        if not m:
            continue
        block = m.group(1)
        alt_datum = re.search(r"<lastmod>([^<]*)</lastmod>", block)
        alt_prio = re.search(r"<priority>([^<]*)</priority>", block)
        alt_d = alt_datum.group(1) if alt_datum else "—"
        alt_p = alt_prio.group(1) if alt_prio else "—"
        if alt_d == datum and alt_p == prio:
            continue
        aenderungen.append((seite, alt_d, datum, alt_p, prio, m))

    if not aenderungen:
        print("Sitemap ist auf dem Stand der Tabelle.")
        return

    for seite, ad, nd, ap, np_, _ in aenderungen:
        teil = []
        if ad != nd:
            teil.append(f"lastmod {ad} → {nd}")
        if ap != np_:
            teil.append(f"priority {ap} → {np_}")
        print(f"  {seite[:46]:46} {', '.join(teil)}")

    if nur_pruefen:
        print(f"\n{len(aenderungen)} Abweichung(en) — mit dem Werkzeug ohne "
              f"--pruefen schreiben.")
        return

    # Von hinten nach vorn ersetzen, damit die Positionen gültig bleiben.
    for seite, _, datum, _, prio, m in sorted(aenderungen,
                                              key=lambda x: -x[5].start()):
        block = m.group(1)

        # Ein einfaches re.sub greift nur, wenn das Element überhaupt da ist.
        # Ein Teil der Einträge wurde ohne <changefreq> und <priority>
        # angelegt — dort muss ergänzt statt ersetzt werden, sonst bleibt die
        # Änderung stillschweigend wirkungslos.
        if "<lastmod>" in block:
            block = re.sub(r"<lastmod>[^<]*</lastmod>",
                           f"<lastmod>{datum}</lastmod>", block)
        else:
            block = block.replace("</loc>", f"</loc><lastmod>{datum}</lastmod>", 1)

        if "<changefreq>" not in block:
            block = re.sub(r"(</lastmod>)", r"\1<changefreq>monthly</changefreq>",
                           block, count=1)

        if "<priority>" in block:
            block = re.sub(r"<priority>[^<]*</priority>",
                           f"<priority>{prio}</priority>", block)
        else:
            block = block.rstrip() + f"<priority>{prio}</priority>"

        roh = roh[:m.start(1)] + block + roh[m.end(1):]

    open(SITEMAP, "w", encoding="utf-8").write(roh)
    print(f"\n{len(aenderungen)} Eintrag/Einträge aktualisiert.")
    print("Danach tools/autorschaft-pflegen.py laufen lassen — es zieht das "
          "sichtbare Datum aus dieser Datei.")


if __name__ == "__main__":
    main()
