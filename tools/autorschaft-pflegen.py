#!/usr/bin/env python3
"""Autorschaft und Aktualität auf den inhaltlichen Seiten ergänzen.

Hintergrund: Bis Ende 2026 sind rund 60 Prozent der kommerziellen
Suchanfragen von KI-Antworten beeinflusst. Diese Systeme zitieren bevorzugt
Inhalte mit erkennbarem Fachautor und nachvollziehbarem Stand. Auf der
Website kamen `author` und `datePublished` bisher auf null von 230 Seiten vor
— Baris stand zwar überall, aber nirgends maschinenlesbar als Fachautor.

Ergänzt wird deshalb dreierlei:

  1. Ein Person-Schema mit fester @id, das die belegbaren Qualifikationen
     trägt: Erlaubnis nach § 34c GewO (Stadt Köln) und § 34i GewO (IHK Köln).
     Nur Angaben aus dem Impressum — nichts Erfundenes.
  2. Ein WebPage-Schema je Seite mit `author`-Verweis auf diese @id und
     `dateModified` aus der Sitemap.
  3. Eine sichtbare Autorenzeile vor dem Schlussaufruf. Sichtbar, weil sowohl
     Google als auch die KI-Systeme den gerenderten Text auswerten und nicht
     nur das Schema.

Ausgenommen bleiben Seiten, bei denen eine Autorschaft nichts aussagt:
Rechtstexte, Formular- und Rechnerseiten, das interne Cockpit.
"""
import json
import os
import re
import sys

WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUSGENOMMEN = {
    "impressum.html", "datenschutz.html", "widerruf.html", "404.html",
    "__forms.html", "lead-cockpit.html", "karriere.html",
    "baufinanzierungsrechner.html", "budget-rechner.html",
}

PERSON_ID = "https://high-seller.de/#baris-oelmez"
FIRMA_ID = "https://high-seller.de/#highseller"

PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "Baris Ölmez",
    "givenName": "Baris",
    "familyName": "Ölmez",
    "jobTitle": "Immobilienmakler und Immobiliardarlehensvermittler",
    "description": ("Inhaber von Highseller Immobilien & Finanzen in Köln. "
                    "Begleitet Eigentümer beim Immobilienverkauf von der Bewertung "
                    "bis zum Notartermin und ist zugleich als unabhängiger "
                    "Immobiliardarlehensvermittler tätig."),
    "image": "https://high-seller.de/assets/img/baris-portrait.jpg",
    "url": "https://high-seller.de/ueber-uns.html",
    "telephone": "+49 162 8811110",
    "email": "info@high-seller.de",
    "worksFor": {"@id": FIRMA_ID},
    "workLocation": {
        "@type": "Place",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Im Zollhafen 18, Kranhaus 1",
            "postalCode": "50678",
            "addressLocality": "Köln",
            "addressCountry": "DE",
        },
    },
    "knowsAbout": [
        "Immobilienbewertung", "Immobilienverkauf", "Baufinanzierung",
        "Immobilienmarkt Köln", "Bodenrichtwerte", "Kapitalanlage Immobilien",
    ],
    "hasCredential": [
        {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Gewerbeerlaubnis",
            "name": "Erlaubnis als Immobilienmakler nach § 34c GewO",
            "recognizedBy": {
                "@type": "GovernmentOrganization",
                "name": "Stadt Köln, Gewerbeabteilung",
            },
        },
        {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Gewerbeerlaubnis",
            "name": "Erlaubnis als Immobiliardarlehensvermittler nach § 34i GewO",
            "recognizedBy": {
                "@type": "GovernmentOrganization",
                "name": "Industrie- und Handelskammer zu Köln",
            },
        },
    ],
    "sameAs": [
        "https://www.tiktok.com/@baris.oelmez",
        "https://www.kleinanzeigen.de/pro/Highseller-Immobilien-Baris-Oelmez",
    ],
}

FIRMA = {
    "@type": "RealEstateAgent",
    "@id": FIRMA_ID,
    "name": "Highseller Immobilien & Finanzen",
    "url": "https://high-seller.de/",
    "founder": {"@id": PERSON_ID},
    "employee": {"@id": PERSON_ID},
}


def sitemap_daten():
    """lastmod je Seite. Die Sitemap wird bei jeder Überarbeitung gepflegt und
    ist damit die verlässlichste Quelle für den Stand — verlässlicher als die
    git-Historie, in der auch reine Umformatierungen stehen."""
    pfad = os.path.join(WURZEL, "sitemap.xml")
    roh = open(pfad, encoding="utf-8").read()
    aus = {}
    for m in re.finditer(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", roh):
        letzt = m.group(1).rstrip("/").split("/")[-1]
        # Die Startseite steht als https://high-seller.de/ in der Sitemap —
        # ohne Dateinamen. Der letzte Pfadteil ist dann der Hostname.
        name = letzt if letzt.endswith(".html") else "index.html"
        aus[name] = m.group(2)
    return aus


def deutsches_datum(iso):
    j, m, t = iso.split("-")
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
              "August", "September", "Oktober", "November", "Dezember"]
    return f"{int(t)}. {monate[int(m) - 1]} {j}"


AUTORBOX = """<section class="section autorzeile-abschnitt"><div class="container">
  <aside class="autorzeile reveal">
    <picture class="autorzeile__bild">
      <source type="image/webp" srcset="assets/img/baris-portrait-450.webp 450w, assets/img/baris-portrait-900.webp 900w" sizes="96px">
      <img decoding="async" src="assets/img/baris-portrait.jpg" alt="Baris Ölmez, Inhaber von Highseller Immobilien &amp; Finanzen" loading="lazy" width="450" height="450">
    </picture>
    <div class="autorzeile__text">
      <p class="autorzeile__rolle">Fachlich verantwortlich</p>
      <p class="autorzeile__name"><a href="ueber-uns.html">Baris Ölmez</a></p>
      <p class="autorzeile__amt">Inhaber von Highseller Immobilien &amp; Finanzen, Köln. Immobilienmakler nach § 34c GewO (Stadt Köln) und Immobiliardarlehensvermittler nach § 34i GewO (IHK zu Köln).</p>
      <p class="autorzeile__stand">Inhalt zuletzt geprüft am <time datetime="{iso}">{lang}</time>. Marktdaten stammen aus amtlichen Quellen; wir aktualisieren sie, sobald neue Jahrgänge vorliegen.</p>
    </div>
  </aside>
</div></section>
"""


def main():
    daten = sitemap_daten()
    os.chdir(WURZEL)
    seiten = [f for f in sorted(os.listdir("."))
              if f.endswith(".html") and f not in AUSGENOMMEN]

    gesetzt = ohne_datum = aktualisiert = 0
    for f in seiten:
        s = open(f, encoding="utf-8").read()
        iso = daten.get(f)

        # Bereits vorhandene Zeile: nur das Datum nachziehen. Ein stehen
        # gebliebenes "zuletzt geprüft am" wäre schlimmer als gar keines —
        # deshalb muss dieses Skript nach jeder Überarbeitung erneut laufen.
        if "autorzeile" in s:
            if not iso:
                continue
            neu_s = re.sub(r'<time datetime="[^"]*">[^<]*</time>',
                           f'<time datetime="{iso}">{deutsches_datum(iso)}</time>', s)
            neu_s = re.sub(r'("dateModified": ")[^"]*(")',
                           lambda m: m.group(1) + iso + m.group(2), neu_s)
            if neu_s != s:
                open(f, "w", encoding="utf-8").write(neu_s)
                aktualisiert += 1
            continue
        if not iso:
            ohne_datum += 1
            continue

        # --- 1. Schema: Person, Firma und Seite als @graph -----------------
        # URL aus canonical, nicht aus dem Dateinamen: Die Startseite ist unter
        # https://high-seller.de/ kanonisch, /index.html leitet dorthin weiter.
        # Ein Schema, das auf die weiterleitende Adresse zeigt, widerspricht
        # dem canonical.
        kan = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        url = kan.group(1) if kan else f"https://high-seller.de/{f}"
        titel = re.search(r"<title>([^<]*)</title>", s)
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                PERSON,
                FIRMA,
                {
                    "@type": "WebPage",
                    "@id": url + "#seite",
                    "url": url,
                    "name": (titel.group(1) if titel else f),
                    "author": {"@id": PERSON_ID},
                    "publisher": {"@id": FIRMA_ID},
                    "dateModified": iso,
                    "inLanguage": "de-DE",
                },
            ],
        }
        block = ('<script type="application/ld+json">'
                 + json.dumps(graph, ensure_ascii=False) + "</script>\n")
        s = s.replace("</head>", block + "</head>", 1)

        # --- 2. Sichtbare Autorenzeile vor dem Schlussaufruf ---------------
        box = AUTORBOX.format(iso=iso, lang=deutsches_datum(iso))
        anker = '<section class="section section--navy">'
        if anker in s:
            s = s.replace(anker, box + anker, 1)
        else:
            s = s.replace("</main>", box + "</main>", 1)

        open(f, "w", encoding="utf-8").write(s)
        gesetzt += 1

    print(f"Autorschaft neu gesetzt auf {gesetzt} Seiten")
    print(f"  Datum nachgezogen: {aktualisiert}   ohne Sitemap-Datum: {ohne_datum}")
    print(f"  ausgenommen: {len(AUSGENOMMEN)} Seiten (Rechtstexte, Rechner, intern)")


if __name__ == "__main__":
    sys.exit(main())
