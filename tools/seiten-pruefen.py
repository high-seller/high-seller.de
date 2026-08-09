#!/usr/bin/env python3
"""
Misst, wie eigenständig eine Seite ist — das Arbeitsinstrument für die
schrittweise Überarbeitung der 231 Seiten.

Hintergrund: Die Website ist Ende Juli von 45 auf über 230 Seiten gewachsen.
Die neuen Seiten entstanden aus Vorlagen, in die je Ort oder Thema Daten
eingesetzt wurden. Das Ergebnis liest sich einzeln gut, in der Masse aber
erkennbar maschinell — und Google wertet massenhaft erzeugte, sich
überlappende Seiten seit der Richtlinie zu "scaled content abuse" ab.

Das Skript misst deshalb vier Dinge, alle am *redaktionellen* Text. Kopfzeile,
Fußzeile, Cookie-Hinweis, Wertrechner-Band und Newsletter-Kasten stehen
technisch identisch auf jeder Seite; wer sie mitzählt, misst Vorlage statt
Inhalt. Genau daran hat sich die frühere Messung schon einmal selbst getäuscht
(rund 20 Prozentpunkte).

  1. Eigenwiederholung — Sätze, die zweimal auf DERSELBEN Seite stehen.
     Der auffälligste Generatorfehler: Ein Datensatz wird in zwei Abschnitte
     ausgegeben, der Leser liest denselben Satz zweimal. Ein Mensch schreibt
     so nicht. Zielwert: 0 %.

  2. Bausteinanteil — Sätze, die wortgleich auf mehr als drei anderen Seiten
     stehen. Ein Sockel davon ist gewollt (Leistungsversprechen, Rechtliches);
     wird er zur Mehrheit des Textes, bleibt kein eigener Inhalt übrig.

  3. Nachbarschaft — die höchste Überlappung mit einer einzelnen anderen Seite,
     gemessen an Fünf-Wort-Ketten. Nennt zusätzlich die nächstverwandte Seite,
     damit man sieht, wer mit wem konkurriert.

  4. Belege — Inhaltsbilder (das Logo zählt nicht), Zahlen, Jahreszahlen,
     Geldbeträge. Eigene Anschauung ist das, was eine Vorlage nicht liefern
     kann.

Aufruf:
    python3 tools/seiten-pruefen.py
        Übersicht aller Seiten, die schwächsten zuerst.

    python3 tools/seiten-pruefen.py wohnung-kaufen-koeln.html
        Einzelbericht: welche Sätze doppelt stehen, welche Bausteine tragen,
        welche Seite am nächsten verwandt ist.

    python3 tools/seiten-pruefen.py --csv > stand.csv
        Für den Verlauf über Monate. Zwei Stände vergleichen zeigt, ob die
        Arbeit an einer Seite die Nachbarn mitverbessert hat.

Ohne Fremdbibliotheken, damit es ohne Einrichtung läuft.
"""

import glob
import html
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Blöcke, die auf jeder Seite technisch identisch stehen. Sie sind kein
# redaktioneller Inhalt und müssen vor jeder Messung heraus.
VORLAGEN_KLASSEN = [
    "valuation-band", "wertband", "footer-newsletter", "mobile-bar",
    "cc", "jumpbar", "breadcrumb", "usp-card",
]

# Seiten, für die der Maßstab nicht gilt: Rechtliches, Formulare, Rechner.
# Sie sollen sich ähneln beziehungsweise haben von Natur aus wenig Fließtext.
AUSGENOMMEN = {
    "impressum.html", "datenschutz.html", "widerruf.html", "404.html",
    "__forms.html", "baufinanzierungsrechner.html", "budget-rechner.html",
    "immobilien-angebote.html", "verkaufte-objekte.html",
}


def _tags_entfernen(s, tags):
    for t in tags:
        s = re.sub(rf"<{t}\b.*?</{t}>", " ", s, flags=re.S | re.I)
    return s


def _klassenbloecke_schneiden(s, klassen):
    """Schneidet <div class="…X…"> … </div> mitsamt Verschachtelung heraus."""
    for cls in klassen:
        while True:
            m = re.search(
                rf'<(div|section)\b[^>]*class="[^"]*\b{re.escape(cls)}\b[^"]*"', s)
            if not m:
                break
            tag = m.group(1)
            i, tiefe = m.end(), 1
            muster = re.compile(rf"</?{tag}\b", re.I)
            while tiefe > 0:
                mm = muster.search(s, i)
                if not mm:
                    i = len(s)
                    break
                tiefe += -1 if s.startswith("</", mm.start()) else 1
                i = mm.end()
            ende = s.find(">", i)
            s = s[:m.start()] + " " + s[ende + 1 if ende > 0 else i:]
    return s


def redaktioneller_text(pfad):
    roh = open(pfad, encoding="utf-8").read()
    a = roh.lower().find("</header>")
    b = roh.lower().rfind("<footer")
    koerper = roh[a + 9:b] if a > 0 and b > a else roh
    koerper = _tags_entfernen(
        koerper, ["script", "style", "svg", "noscript", "form", "select", "template"])
    koerper = _klassenbloecke_schneiden(koerper, VORLAGEN_KLASSEN)
    text = html.unescape(re.sub(r"<[^>]+>", " ", koerper))
    return re.sub(r"\s+", " ", text).strip()


def inhaltsbilder(pfad):
    """Bilder im Inhaltsbereich, ohne Logo — Varianten gelten als ein Motiv."""
    roh = open(pfad, encoding="utf-8").read()
    a = roh.lower().find("</header>")
    b = roh.lower().rfind("<footer")
    koerper = roh[a + 9:b] if a > 0 and b > a else roh
    treffer = re.findall(r'(?:src|data-src)="([^"]*assets/img/[^"]*)"', koerper)
    treffer += re.findall(r"url\(([^)]*assets/img/[^)]*)\)", koerper)
    motive = set()
    for u in treffer:
        name = u.strip("\"' ").split("/")[-1]
        if "logo" in name:
            continue
        # hero-koeln-abend-960.webp und hero-koeln-abend.jpg sind ein Motiv
        motive.add(re.sub(r"-\d+\.(webp|jpg|jpeg|png|avif)$|\.(webp|jpg|jpeg|png|avif)$",
                          "", name))
    return motive


def saetze(text):
    roh = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in roh if len(s.strip()) > 40]


def woerter(text):
    return re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]+", text.lower())


def ketten(ws, n=5):
    return {" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def einlesen():
    seiten = {}
    for pfad in sorted(glob.glob(os.path.join(WURZEL, "*.html"))):
        name = os.path.basename(pfad)
        if name in AUSGENOMMEN:
            continue
        text = redaktioneller_text(pfad)
        ws = woerter(text)
        seiten[name] = {
            "text": text,
            "saetze": saetze(text),
            "woerter": len(ws),
            "ketten": ketten(ws),
            "bilder": inhaltsbilder(pfad),
        }
    return seiten


def bewerten(seiten):
    """Ergänzt je Seite die vier Messwerte."""
    # Wie oft steht ein Satz seitenübergreifend?
    verbreitung = defaultdict(set)
    for name, d in seiten.items():
        for s in set(d["saetze"]):
            verbreitung[s].add(name)

    namen = list(seiten)
    for name in namen:
        d = seiten[name]
        ss = d["saetze"]
        zeichen = sum(len(s) for s in ss) or 1

        haeufig = Counter(ss)
        d["doppelt"] = [(s, n) for s, n in haeufig.items() if n > 1]
        d["eigenwiederholung"] = sum(
            len(s) * (n - 1) for s, n in d["doppelt"]) / zeichen

        d["bausteine"] = sorted(
            ((len(verbreitung[s]), s) for s in set(ss) if len(verbreitung[s]) > 3),
            reverse=True)
        d["bausteinanteil"] = sum(
            len(s) for s in ss if len(verbreitung[s]) > 3) / zeichen

        d["zahlen"] = len(re.findall(r"\b\d[\d.,]*\b", d["text"]))
        d["jahre"] = len(re.findall(r"\b(?:19|20)\d\d\b", d["text"]))
        d["geld"] = len(re.findall(r"(?:€|EUR|Euro)", d["text"]))

    # Nächstverwandte Seite. Quadratisch, aber bei ~220 Seiten in Sekunden durch.
    for i, a in enumerate(namen):
        ka = seiten[a]["ketten"]
        best, bestname = 0.0, "—"
        if ka:
            for b in namen:
                if b == a:
                    continue
                kb = seiten[b]["ketten"]
                if not kb:
                    continue
                wert = len(ka & kb) / min(len(ka), len(kb))
                if wert > best:
                    best, bestname = wert, b
        seiten[a]["nachbar"] = bestname
        seiten[a]["nachbarschaft"] = best


def note(d):
    """Ein Zahlenwert für die Reihenfolge — je höher, desto dringender."""
    return (d["eigenwiederholung"] * 3
            + d["bausteinanteil"]
            + d["nachbarschaft"]
            + (0.4 if not d["bilder"] else 0))


def uebersicht(seiten):
    rang = sorted(seiten.items(), key=lambda x: -note(x[1]))
    print(f"{len(seiten)} Seiten gemessen (Rechtliches und Rechner ausgenommen)\n")
    print(f"{'Seite':<52}{'eigen':>7}{'Baust':>7}{'Nachb':>7}{'Bild':>6}{'Wört':>7}")
    print("-" * 86)
    for name, d in rang[:40]:
        print(f"{name[:51]:<52}"
              f"{d['eigenwiederholung']*100:6.1f}%"
              f"{d['bausteinanteil']*100:6.0f}%"
              f"{d['nachbarschaft']*100:6.0f}%"
              f"{len(d['bilder']):6d}"
              f"{d['woerter']:7d}")
    if len(rang) > 40:
        print(f"… und {len(rang)-40} weitere. Vollständig mit --csv.")

    print("\nMittelwerte über alle gemessenen Seiten:")
    print(f"  Eigenwiederholung {statistics.median(d['eigenwiederholung'] for d in seiten.values())*100:5.1f} %"
          f"   Bausteinanteil {statistics.median(d['bausteinanteil'] for d in seiten.values())*100:5.1f} %"
          f"   Nachbarschaft {statistics.median(d['nachbarschaft'] for d in seiten.values())*100:5.1f} %")
    ohne = sum(1 for d in seiten.values() if not d["bilder"])
    print(f"  Seiten ganz ohne Inhaltsbild: {ohne} von {len(seiten)}")


def einzelbericht(seiten, name):
    if name not in seiten:
        nah = [n for n in seiten if name.rstrip(".html") in n]
        print(f"'{name}' nicht gemessen." +
              (f" Gemeint: {', '.join(nah[:5])}?" if nah else ""))
        return 1
    d = seiten[name]
    print(f"=== {name} ===")
    print(f"{d['woerter']} Wörter redaktioneller Text, "
          f"{len(d['bilder'])} Inhaltsbild(er), "
          f"{d['zahlen']} Zahlen, {d['jahre']} Jahreszahlen, {d['geld']} Geldangaben")
    print(f"Nächstverwandt: {d['nachbar']} ({d['nachbarschaft']*100:.0f} % gemeinsame Wortketten)")

    print(f"\n-- Eigenwiederholung: {d['eigenwiederholung']*100:.1f} % --")
    if d["doppelt"]:
        for s, n in sorted(d["doppelt"], key=lambda x: -len(x[0])):
            print(f"  {n}x  {s[:150]}")
    else:
        print("  keine — gut.")

    print(f"\n-- Bausteinanteil: {d['bausteinanteil']*100:.0f} % --")
    for n, s in d["bausteine"][:12]:
        print(f"  auf {n:3d} Seiten  {s[:130]}")
    if not d["bausteine"]:
        print("  keine Sätze, die auf mehr als drei Seiten stehen.")

    if d["bilder"]:
        print(f"\n-- Bilder --")
        for b in sorted(d["bilder"]):
            print(f"  {b}")
    else:
        print("\n-- Bilder: keine. Das ist der größte einzelne Mangel. --")
    return 0


def csv_ausgabe(seiten):
    print("seite;eigenwiederholung;bausteinanteil;nachbarschaft;nachbar;bilder;woerter;zahlen;jahre;geld")
    for name, d in sorted(seiten.items()):
        print(f"{name};{d['eigenwiederholung']:.4f};{d['bausteinanteil']:.4f};"
              f"{d['nachbarschaft']:.4f};{d['nachbar']};{len(d['bilder'])};"
              f"{d['woerter']};{d['zahlen']};{d['jahre']};{d['geld']}")


def main():
    seiten = einlesen()
    if not seiten:
        print("Keine Seiten gefunden. Läuft das Skript im Projektverzeichnis?")
        return 1
    bewerten(seiten)

    argumente = [a for a in sys.argv[1:]]
    if "--csv" in argumente:
        csv_ausgabe(seiten)
        return 0
    if argumente:
        return einzelbericht(seiten, argumente[0])
    uebersicht(seiten)
    return 0


if __name__ == "__main__":
    sys.exit(main())
