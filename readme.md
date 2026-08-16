# Highseller Immobilien & Finanzen — Website (Stand v63)

## Was in v63 umgesetzt wurde

### Zollstock und Klettenberg ausgebaut — zwei gegensätzliche Befunde

Beide waren mit rund 1.670 Wörtern die kürzesten der neun ausgebauten Seiten.
Jetzt: **Zollstock 2.120, Klettenberg 2.145 Wörter.** Zahlen 90 → 133
beziehungsweise 133 → 176, Geldangaben 36 → 32 und 22 → 42.

Beiden fehlten dieselben drei Themen, die die neueren Seiten tragen: Mieten,
Kaufpreisfaktor und die Einordnung in die Stadtentwicklung. Die Aufhänger sind
dabei das genaue Gegenteil voneinander.

**Zollstock: Kölns drittgrößte Baustelle — mit den kleinsten Wohnungen.**
338 fertiggestellte Wohnungen 2025 sind Rang 3 unter allen 87 Stadtteilen,
hinter Marienburg (568) und der Innenstadt (410). Zugleich steht der Stadtteil
bei der Wohnungsgröße auf **Rang 77**: 64,6 m² gegen 77,3 in Köln, bei 58,3 %
Einpersonenhaushalten (Rang 10). Daraus folgt eine klare Ansage für
Eigentümer: Wer eine größere Bestandswohnung verkauft, konkurriert kaum mit
diesen 338 Einheiten — die Käufergruppe ist eine andere. Wer eine kleine
verkauft, steht dagegen in direkter Konkurrenz zu Erstbezug. Neu ist außerdem,
dass Zollstock zum Plangebiet der Parkstadt Süd gehört.

**Klettenberg: der Stadtteil, in dem fast nicht gebaut wird.** Neun neue
Wohnungen im ganzen Jahr bei 5.693 Bestandswohnungen — 0,16 Prozent, Rang 66.
Der Anteil geförderter Wohnungen liegt bei **null** (Rang 3 von 87). Und der
Bodenrichtwert schwankt über den Stadtteil praktisch nicht: 1.590 und 1.650 €
sind **Faktor 1,04**, Rang 3 der homogensten unter 81 Stadtteilen mit mehreren
Zonen. Homogener sind nur Gremberghoven und Finkenberg — beides günstige
Randlagen. Zum Vergleich: Junkersdorf 2,43, Rodenkirchen 2,45, Müngersdorf
2,55.

Für Verkäufer heißt das zweierlei, und beides steht auf der Seite: Knappheit
als Argument (kaum Neubaukonkurrenz), aber auch wenige Vergleichswerte — bei
49 beurkundeten Verkäufen im Jahr verschiebt ein einzelner ungewöhnlicher Fall
den Durchschnitt spürbar.

**Der Renditevergleich fällt entsprechend aus:** Zollstock 24,8 Jahresmieten
und 4,04 % brutto (über dem Kölner Mittel von 3,80 %), Klettenberg 30,3 und
3,30 % (darunter). Daraus folgt die Käufergruppe — in Zollstock sind
Kapitalanleger eine ernsthafte Zielgruppe, in Klettenberg kaufen überwiegend
Selbstnutzer, die nicht die Rendite bezahlen, sondern den Stadtteil.

**Geprüft:** Tag-Balance über fünf Elementtypen, alle Sprungziele auf Existenz,
keine doppelten IDs, Lighthouse mobil 100/100/100/100 auf beiden Seiten,
FAQ-Schema unverändert stimmig (81 Seiten).

**Cache-Buster:** `styles.css?v=78` auf allen 231 Seiten.

## Was in v62 umgesetzt wurde

### Sprungnavigation auf allen neun ausgebauten Veedelseiten

Die `.jumpbar` steht jetzt auf allen neun statt bisher drei. Die sechs
älteren Seiten konnten sie vorher nicht bekommen, weil ihren
`<section>`-Elementen die `id` fehlte: Deutz und Zollstock hatten gar keine,
Sülz eine, Ehrenfeld und Klettenberg je drei, Lindenthal vier. Diese Seiten
sind zwischen 1.664 und 2.767 Wörter lang — ohne Navigation heißt das für
Leser: scrollen, bis man findet, was man sucht.

**39 Abschnitts-IDs vergeben**, je Seite sechs Sprungziele. Die IDs sind von
Hand gewählt statt aus den Überschriften abgeleitet: Automatisch erzeugte
Kürzel aus Sätzen wie „Der Höchststand war 2023 — und er ist vorbei" wären
lang und unleserlich, und sie sind dauerhafte Sprungadressen, die auch in
Verweisen von außen auftauchen können.

Das Werkzeug liegt als `tools/sprungleisten-setzen.py` im Repo. Es findet die
Abschnitte über ihre Überschriften, vergibt die IDs und setzt die Leiste hinter
den Kopfbereich, damit der Aufmacher unverstellt bleibt.

**Geprüft:** Alle 54 Sprungziele auf Existenz, keine doppelten IDs,
Tag-Balance über vier Elementtypen auf allen neun Seiten, drei Sprünge je
Seite im Browser durchgeklickt (Ziel landet 141 px unter der Leiste, aktiver
Eintrag wird korrekt markiert), Karte und Bodenanteil-Rechner auf Lindenthal
unbeschädigt, Lighthouse mobil 100/100/100/100 auf Deutz, Lindenthal und
Zollstock.

**Cache-Buster:** `styles.css?v=77` auf allen 231 Seiten.

## Was in v61 umgesetzt wurde

### 238 Fragen, die sichtbar auf der Website standen, aber für Suchmaschinen unsichtbar waren

Beim Vergleich der Veedelseiten fiel auf, dass mehrere Seiten Fragen und
Antworten im Text tragen, ohne dass diese im strukturierten Datensatz
auftauchen. Die Prüfung über alle 233 Seiten ergab: **Nur 22 Seiten hatten
überhaupt ein FAQPage-Schema**, obwohl 87 Seiten sichtbare FAQ-Bereiche haben.

Für Leser macht das keinen Unterschied. Für Suchmaschinen entfällt damit die
Chance auf erweiterte Suchergebnisse, in denen die Fragen direkt unter dem
Treffer erscheinen — bei einer Website, deren Stärke Fachfragen sind, ein
erheblicher Verlust.

Neu ist `tools/faq-schema-pflegen.py`. Es liest die sichtbaren Fragen in den
**drei Bauarten**, die auf der Website vorkommen, und schreibt sie ins Schema:

- `<details class="faq-item">` mit `<summary>` — die neueren Veedelseiten
- `<dl>` mit `<dt>`/`<dd>` — die Themenseiten
- `<h3>` mit Folgeabsätzen — Deutz, Sülz, Zollstock

Ergebnis: **87 Seiten mit FAQPage statt 22, 260 Fragen im Schema**, davon 254
verschiedene. Keine Frage steht auf mehr als drei Seiten — die FAQ sind
durchgehend seitenspezifisch, es entsteht kein Duplikat.

### Zwei Fehler beim ersten Anlauf — beide gefunden, bevor sie live gingen

**1. Zwischenüberschriften als Fragen.** Der erste Parser übernahm alles, was
als `<h3>` in einem FAQ-Abschnitt stand — auch „Was wir übernehmen" und
„Makler und Finanzierer in einem". Auf 60 Seiten wären damit 240 falsche
Einträge ins Schema gewandert. Für Suchmaschinen ist eine irreführende
Auszeichnung schlechter als gar keine. Der Lauf wurde zurückgerollt und das
Werkzeug um eine Prüfung ergänzt: **Nur was auf ein Fragezeichen endet, gilt
als Frage.**

**2. Zwei FAQPage-Knoten auf einer Seite.** Marienburg trug bereits einen
eigenständigen FAQPage-Block mit zwei alten Fragen; beim Ausbau kam ein
zweiter im `@graph`-Knoten hinzu. Zwei Auszeichnungen sind kein doppelter
Nutzen — für Suchmaschinen ist dann nicht bestimmt, welche gilt. Der alte
Block ist entfernt, und das Werkzeug meldet solche Doppelungen jetzt
ausdrücklich.

**Geprüft:** JSON aller 233 Seiten auf Gültigkeit, Tag-Balance über sechs
Elementtypen auf allen 68 geänderten Seiten, keine Seite mit mehr als einem
FAQPage-Knoten, Stichprobe der Schemainhalte gegen den sichtbaren Text,
Lighthouse mobil 100/100/100/100.

**Cache-Buster:** `styles.css?v=76` auf allen 231 Seiten.

## Was in v60 umgesetzt wurde

### Marienburg auf das Niveau der übrigen Seiten gebracht

Marienburg war nach dem ersten Ausbau die schwächste der ausgebauten Seiten:
1.757 Wörter gegen 2.219 bei Raderthal, nur zwei Bilder statt vier — und als
einzige **ohne bedienbares Element**. Raderthal hat den Unterlagen-Prüfer,
Raderberg den Mikrolagen-Wähler; hier fehlte das Gegenstück.

Jetzt: **2.334 Wörter, 116 Zahlen, 28 Geldangaben, vier Bilder** — und ein
Rechner, der genau zur Kernaussage der Seite passt.

**Der Bodenwert-Rechner.** Zwei Schieberegler für Grundstücks- und
Wohnfläche, gerechnet wird ausschließlich mit dem amtlichen Bodenrichtwert von
2.100 Euro und dem Median der Kölner Wohnungsverkäufe — keine geschätzten
Faktoren. Ausgegeben werden der reine Bodenwert, der Anteil je Quadratmeter
Wohnfläche und ein Satz, der sich mitverändert: Bei 700 m² Grundstück und
250 m² Wohnfläche ist der Boden allein mehr wert als die gesamte Wohnfläche
zum Wohnungspreis. Bei 400 m² sind es 59 Prozent. Der Fußtext sagt
ausdrücklich, dass das **keine Bewertung** ist und was in der Rechnung fehlt.

**Zwei neue Kapitel.** Denkmalschutz — als Gegenüberstellung von
Einschränkungen (Erlaubnispflicht, aufwendigere energetische Modernisierung,
Ensembleschutz) und Wert (erhöhte Absetzung nach §§ 7i und 10f EStG, nicht
nachbaubare Substanz, gesichertes Umfeld). Und die Käufergruppen, weil bei
siebenstelligen Kaufpreisen nicht die Zahl der Anfragen zählt, sondern welche.

**Viertes Bild:** der Südpark, die Lage, die in Baris' Vorlage ausdrücklich
vorkommt.

### Ein Strukturfehler beim Einbau — gefunden und behoben

Beim Einfügen des vierten Bildes wurde ein zusätzliches `</div></section>`
gesetzt, obwohl der Abschnitt an dieser Stelle bereits geschlossen war.
Ergebnis: 14 öffnende gegen 15 schließende `section`-Tags und ein Bild, das
zwischen zwei Abschnitten hing. Die Tag-Balance-Prüfung nach jedem Einbau hat
das sofort gezeigt — ohne sie wäre es live gegangen. **Nach jedem
Skript-Einbau die Tags zählen, nicht nur die Seite ansehen.**

**Geprüft:** Lighthouse mobil 100/100/100/100 (59 bestandene Prüfungen), alle
vier Reglerstellungen des Rechners durchgerechnet, Tag-Balance über neun
Elementtypen, alle sieben Sprungziele auf Existenz geprüft.

**Cache-Buster:** `styles.css?v=75` und `main.js?v=37` auf allen 231 Seiten.

## Was in v59 umgesetzt wurde

### Köln-Marienburg ausgebaut

Neunte Veedelseite, **564 auf 1.757 Wörter** redaktionellen Text. Zahlen 37 →
**112**, Geldangaben 4 → **26**, Bilder 1 → 3, Eigenwiederholung bleibt bei 0 %.

**Der Aufhänger widerspricht dem Image des Stadtteils vollständig — und ist
eindeutig belegt: Marienburg ist Kölns größte Wohnbaustelle.** 568
fertiggestellte Wohnungen 2025 sind **Rang 1 unter allen 87 Stadtteilen**,
absolut wie gemessen am Bestand (12,9 Prozent Zuwachs in einem Jahr).
Gleichzeitig bleibt es das Villenviertel: Rang 2 in Köln bei der Wohnfläche je
Einwohner (65,9 m² gegen 40,6 in Köln).

Daraus folgt die Aussage der Seite, die Baris' Schlusssatz („Marienburg
verkauft man nicht nach Schema F") mit Zahlen unterlegt: **Der Stadtteil hat
zwei Märkte.** Bestandswohnungen 5.684 €/m² aus 47 Kaufverträgen, Neubau
9.888 €/m² aus elf — dazwischen liegen 4.204 € je Quadratmeter oder über
630.000 € bei einer 150-m²-Wohnung. Ein gemittelter Quadratmeterpreis
beschreibt keine der beiden Wirklichkeiten.

**Woher die 568 Wohnungen kommen, ist recherchiert:** „Die Welle" am
Raderberggürtel 50, dem früheren Gelände der Deutschen Welle — 752 Wohnungen
in drei Baufeldern (257, 249, 246), davon 70 öffentlich gefördert, dazu rund
6.100 m² Gewerbefläche und eine Kita mit sechs Gruppen, Fertigstellung 2026.
Ein einzelnes Projekt fügt einem Stadtteil mit 4.416 Wohnungen also gut ein
Sechstel hinzu.

**Der zweite Befund ist der amtliche Beleg für Baris' Kernfrage.** Marienburg
ist einer von nur **vier** Kölner Stadtteilen mit einer **einzigen**
Bodenrichtwertzone (2.100 €). Dellbrück hat fünfzehn, Rath-Heumar und Brück je
vierzehn. Der amtliche Bodenwert kann in Marienburg also gar nicht zwischen
der ruhigen Villenlage und dem Grundstück an der Hauptstraße unterscheiden.

Daran schließt das Rechenbeispiel an: Bei 2.100 € je m² Grundstück liegt der
**reine Bodenwert** eines 700-m²-Grundstücks bei 1,47 Millionen Euro — mehr
als die 1,42 Millionen, die der Wohnungs-Quadratmeterpreis für 250 m²
Wohnfläche ergäbe. Ein Villengrundstück lässt sich mit einem Wohnungspreis
nicht bewerten.

### Ein eigener Fehler auf der Raderberg-Seite korrigiert

Das dort verwendete Luftbild zeigt das frühere Deutsche-Welle-Gelände. Die
Bildunterschrift ließ die geräumte Fläche als Teil Raderbergs erscheinen —
tatsächlich liegt sie am Raderberggürtel **50** und gehört zu Marienburg,
während das Funkhaus des Deutschlandfunks an Nummer **40** in Raderberg steht.
Bildunterschrift und Alt-Text benennen die Stadtteilgrenze jetzt und verlinken
nach Marienburg. Aufgefallen ist das erst bei der Recherche zu „Die Welle".

### Zwei Fehler, die erst der Live-Test zeigte

**1. Die Einblendung machte jeden Text kurzzeitig unlesbar.** `.reveal` fuhr
die Deckkraft über 0,6 Sekunden von 0 auf 1. In diesem Fenster hat jeder Text
darin zu wenig Kontrast — Lighthouse maß auf der Live-Seite Werte bis
**1,79:1**, auch auf Schaltflächen. Dunklere Farben lösen das nicht: Bei
Deckkraft 0,3 hilft keine Farbe mehr. Die Animation blendet deshalb nicht mehr
auf, sondern lässt die Elemente nur noch hereingleiten (`transform`, 28 statt
22 Pixel). Der Effekt bleibt sichtbar, der Text ist zu jedem Zeitpunkt lesbar.
Das betrifft alle 231 Seiten.

**2. Namenskonflikt im Stylesheet.** Das Kürzel `mb-` war bereits vom
**Marktbericht** belegt (88 Klassen). Für Marienburg dasselbe zu wählen war
ein Fehler: Beide Seiten definierten `mb-kopf` und `mb-kopf__lead` mit
verschiedenen Farben, und welche gewann, hing allein an Spezifität und
Reihenfolge. Sichtbar wurde es an der Augenbraue des Marienburg-Kopfes, die im
Blau des Marktberichts erschien statt im Grünton. Marienburg trägt jetzt
durchgehend `mrb-` — 20 Klassen in HTML und Stylesheet umbenannt, die
Marktbericht-Regeln unberührt.

**Geprüft:** Lighthouse mobil 100/100/100/100 (59 bestandene Prüfungen),
Kollisionsprüfung der Diagrammbeschriftungen, kein seitlicher Überlauf,
Sprungleiste mit sechs Zielen, Sitemap und Fußzeile über die Werkzeuge
gepflegt — Marienburg jetzt von 230 Seiten verlinkt.

**Cache-Buster:** `styles.css?v=73` auf allen 231 Seiten.

## Was in v58 umgesetzt wurde

### Raderberg vertieft — jetzt die stärkste Veedelseite

Die Seite war nach ihrem ersten Ausbau messbar schwächer als die älteren:
1.970 Wörter gegen 2.000 bis 2.800, 65 Zahlen gegen 90 bis 158 und nur acht
Geldangaben gegen 26 bis 37. Jetzt steht sie mit **2.968 Wörtern, 128 Zahlen
und 30 Geldangaben** an der Spitze aller acht ausgebauten Seiten — vor Deutz.

**Die Parkstadt Süd bekommt ein eigenes Kapitel mit belegten Zahlen** — und
mit dem Punkt, den Werbetexte auslassen: Das Vorhaben ist **noch nicht
beschlossen, sondern in Planung**. Der Aufstellungsbeschluss datiert vom
7. November 2024, die frühzeitige Öffentlichkeitsbeteiligung lief vom
26. Februar bis 21. März 2025. Belegt sind außerdem 115 Hektar Planungsgebiet,
46 Hektar im laufenden Bebauungsplan, rund 3.400 Wohneinheiten für etwa 7.700
Menschen, 4.300 Arbeitsplätze und über 30 Hektar Zuwachs für den Inneren
Grüngürtel.

Daraus folgt die **Drei-Phasen-Darstellung**, die den eigentlichen Wert der
Seite ausmacht: Heute ist die Fläche Planungsgebiet und ein Käufer zahlt für
Ankündigungen nichts. In der Bauphase prägen Baustellenverkehr und Lärm das
Umfeld — die schwierigste Zeit für einen Verkauf in unmittelbarer Nähe. Nach
Fertigstellung ist die Infrastruktur da, aber Tausende neue Wohnungen stehen
im Wettbewerb. Das ist die ehrliche Antwort auf die Frage, ob die Parkstadt
Süd gut für den eigenen Verkaufspreis ist, und sie lautet: kommt darauf an,
wann.

**Neu ist auch der Vergleich der drei betroffenen Stadtteile.** Das Plangebiet
liegt in Zollstock, Raderberg und Bayenthal — und die stehen wirtschaftlich
weit auseinander: Bayenthal hat mit 2.830 € fast den doppelten Bodenrichtwert
Raderbergs, aber nur 16 Prozent höhere Wohnungspreise. Zollstock ist mit
23.729 Einwohnern und 338 fertigen Wohnungen 2025 das Volumen, mit dem
Raderberger Verkäufer konkurrieren.

**Die greifbarste Zahl der Seite:** Wer in Raderberg 500.000 Euro ausgibt,
bekommt im Bestand rund 98 Quadratmeter — im Neubau nur 68. Dazu kommen
Rechenbeispiele für 60, 80 und 100 Quadratmeter sowie eine Überschlagsrechnung
zum Bodenanteil am Kaufpreis (15 bis 25 Prozent je nach Bebauungsdichte).

### Sprungnavigation auf den beiden langen Seiten

Raderberg war auf **22 Bildschirmhöhen** gewachsen — ohne Navigation heißt das
für Leser: scrollen, bis man findet, was man sucht, oder aufgeben. Die
`.jumpbar` existierte bereits vollständig (sticky, mit Markierung des aktiven
Abschnitts), wurde aber nur auf der Startseite verwendet. Sie steht jetzt auch
auf Raderberg und Raderthal, jeweils mit sechs Zielen und bewusst **hinter**
dem Aufmacher, damit der Kopf unverstellt bleibt.

**Auf den sechs älteren Veedelseiten geht das noch nicht:** Deutz und Zollstock
haben gar keine Abschnitts-IDs, Sülz eine, Ehrenfeld und Klettenberg je drei,
Lindenthal vier. Dort wäre erst eine Strukturierung nötig — ein eigener
Arbeitsschritt.

### Was nicht möglich war

Eine Karte, wie sie die sechs älteren Veedelseiten haben, ließ sich nicht
bauen. Die BORIS-Rohdaten liegen nicht im Worktree (400 MB, in `.gitignore`),
und weder opengeodata.nrw.de noch die OSM-Hauptschnittstelle noch das
Geoportal der Stadt Köln waren aus dieser Umgebung erreichbar. Eine nach
Augenmaß gezeichnete Karte wäre schlechter als keine — dieser Fehler ist bei
Deutz schon einmal gemacht worden. Der Ausbau ging deshalb in Daten und
Recherche statt in Geometrie.

**Geprüft:** Lighthouse mobil 100/100/100/100 auf beiden Seiten (Raderberg
jetzt 59 statt 56 bestandene Prüfungen), kein seitlicher Überlauf,
Kollisionsprüfung aller Diagrammbeschriftungen, Sprungleiste auf Kleben und
aktive Markierung getestet.

**Cache-Buster:** `styles.css?v=70` auf allen 231 Seiten (`main.js` unverändert
bei v=36).

## Was in v57 umgesetzt wurde

### Köln-Raderberg ausgebaut

Achte Veedelseite, **682 auf 1.902 Wörter** redaktionellen Text.
Eigenwiederholung 10,9 → **0,0 %**, Bausteinanteil 23 → **3 %**, Bilder 1 → 3.
Grundlage waren fünf Textvorlagen von Baris, verdichtet statt übernommen.

**Der Aufhänger ist für Köln einzigartig.** Raderberg hat 2025 insgesamt
**234 Wohnungen fertiggestellt** — bei 3.990 Bestandswohnungen sind das 5,86
Prozent Zuwachs in einem einzigen Jahr und **Rang 3 unter allen 87 Kölner
Stadtteilen** (hinter Marienburg und Elsdorf). Und der große Teil kommt erst:
Die Parkstadt Süd bringt ab 2030 über 3.000 Wohneinheiten, wodurch Raderberg
laut amtlicher Vorausberechnung bis 2035 **seine Bevölkerung verdoppelt**.

Die ehrliche Einordnung dieser Zahl trägt die Seite — und sie stammt aus
Baris' eigenem Text: „Aus einer großen Stadtentwicklung lässt sich nicht
automatisch der Wert Ihrer einzelnen Immobilie ableiten." Genau so steht es
dort: Wer 2030 verkauft, konkurriert mit Tausenden neuen Wohnungen, die genau
die Käufer ansprechen, die Erstbezug und aktuellen Energiestandard suchen. Die
Parkstadt Süd ist für Eigentümer deshalb vor allem ein **Grund, den
Verkaufszeitpunkt bewusst zu wählen** — keine pauschal gute Nachricht.

**Zweiter Befund:** Der Abstand zwischen Neubau (7.309 €/m²) und Bestand
(5.113 €/m²) beträgt in Raderberg nur 43 Prozent. Für Kölner Verhältnisse ist
das gering — Junkersdorf liegt bei 130 Prozent, Brück bei 114. Der Bestand ist
hier also gut bewertet und gilt Käufern als eigenständige Alternative, nicht
als billigere Notlösung.

**Blickfang ist ein Mikrolagen-Wähler** über die vier Straßen aus Baris'
Vorlage: Kreuznacher, Brühler, Mannsfelder und Raderberger Straße. Je Lage
zeigt er, welche Eigenschaften dort über den Preis entscheiden, welche
Käufergruppe zuerst hinschaut und was daraus für die Vermarktung folgt. Damit
wird sein Kerngedanke bedienbar: Käufer erleben keine Durchschnittslage.

### Ein SEO-Fehler in beiden Wählern behoben

Der Unterlagen-Prüfer (Raderthal) und der Mikrolagen-Wähler (Raderberg) bauten
ihren Inhalt **ausschließlich per JavaScript** auf. Im ausgelieferten HTML
standen nur die Knöpfe. Für Leser funktioniert das, für Suchmaschinen ist es
schlechter: Google rendert JavaScript zwar, aber verzögert und ohne Garantie —
Inhalt, der ranken soll, gehört ins Markup.

Beide Elemente liefern jetzt ihre erste Ansicht direkt im HTML aus; das Skript
überschreibt sie beim ersten Klick. Für Raderthal sind das zehn Unterlagen mit
Herkunft, für Raderberg die vollständige Tafel zur Kreuznacher Straße. Die
Darstellung ändert sich nicht, nur der Auslieferungszustand.

### Sichtbarkeitswerkzeuge vervollständigt

`tools/fusszeile-standorte.py` liegt jetzt im Repo (vorher nur im
Arbeitsverzeichnis) und leitet seinen Pfad selbst ab. Zusammen mit
`tools/sitemap-pflegen.py` sind damit beide Schritte nach jeder Überarbeitung
wiederholbar:

    python3 tools/sitemap-pflegen.py        # lastmod und priority
    python3 tools/fusszeile-standorte.py    # interne Verlinkung
    python3 tools/autorschaft-pflegen.py    # sichtbares Datum

Alle acht ausgebauten Seiten sind jetzt von 230 Seiten verlinkt und stehen auf
`priority 0.8`.

### Eine Falle bei dieser Seite

**Ein flacher Balken trägt keine zwei Textzeilen.** In der Bautreppe standen
Zahl und Beschreibung übereinander im Balken. Beim niedrigsten Balken (234
Wohnungen, 30 Prozent der Höhe) reichte der Platz nicht, und die
Beschriftungen überlappten — sichtbar erst in der Kollisionsprüfung am
gerenderten SVG, nicht im Stylesheet. Jetzt steht nur die Zahl im Balken,
alles Weitere darunter.

**Nicht übernommen:** die „rund 750 Banken" aus den Vorlagen (unbelegt,
§ 5a UWG — diesmal viermal genannt).

**Geprüft:** Lighthouse mobil 100/100/100/100 auf Raderberg und Raderthal,
kein seitlicher Überlauf, alle vier Lagen des Wählers durchgeklickt,
Startansicht im HTML gegen das Skript geprüft.

**Cache-Buster:** `styles.css?v=69` und `main.js?v=36` auf allen 231 Seiten.

## Was in v56 umgesetzt wurde

### Köln-Raderthal ausgebaut

Siebte Veedelseite, von **577 auf 2.123 Wörter** redaktionellen Text.
Eigenwiederholung 10,4 → **0,0 %**, Bausteinanteil 25 → **3 %**, Bilder 1 → 3.
Grundlage waren acht Textvorlagen von Baris, verdichtet statt übernommen —
so ausdrücklich gewünscht.

**Der Aufhänger kommt wieder aus den Daten.** Raderthal hat keinen einzigen
Spitzenwert: Rang 42 von 87 bei der Wohnungsgröße, Rang 25 beim
Durchschnittsalter, Rang 55 bei den Haushalten mit Kindern, Rang 20 beim
Wohnungspreis. Ein Stadtteil der Mittelwerte.

Genau das trägt die Seite. Denn Baris' eigener Verkauf in der Hitzelerstraße
lag mit **5.506 €/m² neunzehn Prozent über** dem amtlichen Stadtteilmedian von
4.628 €/m². Und der Bodenrichtwert schwankt innerhalb Raderthals zwischen
1.090 und 1.770 € — **Faktor 1,62 in einem einzigen Stadtteil**. Beides belegt
denselben Satz, der sich durch alle acht Vorlagen zieht: Der Durchschnitt sagt
nichts über die einzelne Immobilie.

**Blickfang ist ein Unterlagen-Prüfer.** Aus der längsten Vorlage (einer sehr
langen Aufzählung) wurde ein bedienbares Element: Objektart wählen, und die
Liste zeigt, was gebraucht wird — mit Herkunft je Posten. Haus 10, Wohnung 12,
Grundstück 7, Mehrfamilienhaus 11 Unterlagen. Beim Grundstück entfallen
Energieausweis, Grundrisse und Wohnflächenberechnung automatisch.

**Drei echte Verkaufsfälle** stehen erstmals auf einer Veedelseite: die
Hitzelerstraße mit ihrem Aufschlag, der Vergleich zweier Grundstücke
(Raderthal rund ein Monat, Bayenthal deutlich länger wegen
Bodenverunreinigungen) und die Markusstraße, wo ein Käufer an fehlenden
Unterlagen scheiterte. Das ist genau das Material, das den Seiten bisher
fehlte — Erfahrungswissen, das kein Wettbewerber abschreiben kann.

**Nicht übernommen** wurden die „rund 750 Finanzierungspartner" (unbelegt,
§ 5a UWG — in den Vorlagen dreimal genannt) sowie alles, was Rechtsberatung
wäre. Der Abschnitt zu Notarkosten nennt die Unterscheidung und verweist für
die verbindliche Auskunft ans Notariat.

### Sichtbarkeit der überarbeiteten Seiten — zwei stille Fehler behoben

Phillip hatte darum gebeten, dass die überarbeiteten Seiten auch tatsächlich
in die Sichtbarkeit kommen. Die Prüfung förderte zwei Befunde zutage:

**1. Veraltete `lastmod`-Daten.** Ehrenfeld, Lindenthal und Klettenberg
standen nach ihrer Überarbeitung noch auf dem 28. Juli. Das wirkt doppelt: Ein
`lastmod` vor dem Änderungsdatum sagt Google, an der Seite habe sich nichts
getan — und `tools/autorschaft-pflegen.py` liest dasselbe Datum aus, um es als
sichtbares „zuletzt geprüft am" auf die Seite zu schreiben. Es stand also auch
für Leser das falsche Datum da.

Dafür gibt es jetzt **`tools/sitemap-pflegen.py`** mit einer Tabelle der
inhaltlichen Überarbeitungsstände. Das Commit-Datum taugt dafür nicht: Ein
Cache-Buster-Lauf fasst alle 231 Dateien an, ohne einen Inhalt zu ändern.
Aufruf mit `--pruefen` meldet nur Abweichungen. Ausgebaute Seiten stehen jetzt
auf `priority 0.8`, der Marktbericht auf 0.9 statt gemeinsam mit 167 anderen
auf 0.7.

**2. Ungleiche interne Verlinkung.** Die Fußzeile trug vier feste Verweise —
Köln, Lindenthal, Sülz, Ehrenfeld — plus einen Selbstverweis. Ergebnis:
Lindenthal, Sülz und Ehrenfeld waren von 230 Seiten verlinkt, **Deutz aber nur
von 14, Zollstock von 16, Klettenberg von 17 und Raderthal von 11.**
Ausgerechnet die aufwendig ausgebauten Seiten bekamen also das geringste
interne Gewicht. Die feste Liste enthält jetzt alle sieben ausgebauten Veedel;
alle sind von 230 Seiten verlinkt.

### Zwei Fallen bei dieser Seite

- **Beschriftungen im SVG kollidieren, wenn Werte dicht beieinanderliegen.**
  Auf der Bodenrichtwert-Skala überlappte „1.220 €" (Median) mit „1.090 €"
  (günstigste Zone), weil beide auf einer Achse von 950 bis 1.900 nur
  130 Euro auseinanderliegen. Der Median sitzt jetzt auf einer eigenen Ebene
  unterhalb, angebunden mit einer gestrichelten Linie. Im Stylesheet ist so
  etwas nicht zu sehen — es braucht eine Kollisionsprüfung am gerenderten
  Element.
- **`re.sub` ersetzt nichts, wenn das Element fehlt.** Das erste
  Sitemap-Werkzeug setzte `priority` bei drei Einträgen scheinbar erfolgreich,
  obwohl diese Einträge gar kein `<priority>` hatten. Die Meldung sagte
  „geändert", die Datei blieb gleich. Jetzt wird ergänzt statt nur ersetzt.

**Geprüft:** Lighthouse mobil 100/100/100/100, kein seitlicher Überlauf, alle
vier Objektarten des Prüfers durchgeklickt, Fußzeile auf 231 Seiten
kontrolliert, `sitemap.xml` als XML validiert.

**Cache-Buster:** `styles.css?v=68` und `main.js?v=35` auf allen 231 Seiten.

## Was in v55 umgesetzt wurde

### Marktbericht auf Kampmeyer-Niveau ausgebaut

Der Bericht deckte bisher nur den Kaufmarkt ab. Das war der Grund, warum er
neben dem Marktbericht von Kampmeyer kürzer und dünner wirkte: Dort stehen
Mieten, Prognosen und Neubauprojekte, hier standen sie nicht. Der Bericht ist
von rund 2.900 auf **über 5.100 Wörter** gewachsen, die Zahl der belegten
Angaben von 259 auf **499**.

**Drei neue Kapitel, beide Quellen amtlich:**

- `#mieten` — Grundlage ist *Kölner Statistische Nachrichten 9/2026, „Das
  Mietwohnungsangebot in Köln 2025"* (Amt für Stadtentwicklung und Statistik,
  Juni 2026). Ausgewertet sind dort 12.205 Mietangebote, davon 11.659
  verwertbar. Median der Angebotsmieten 2025: **14,70 €/m²** nettokalt, +5 %
  gegenüber 14,00 € im Vorjahr.
- `#rendite` — Kaufpreisfaktoren, aus zwei amtlichen Quellen selbst gerechnet:
  Kaufpreis je m² (Gutachterausschuss, Weiterverkäufe) geteilt durch zwölf
  Monatsmieten je m² (KSN 9/2026).
- `#bevoelkerung` — *KSN 12/2025, „Bevölkerungsvorausberechnung für Köln 2025
  bis 2045"*, Basisvariante, kleinräumig bis 2035.

**Die Befunde, die den Bericht tragen — alle nachrechenbar:**

- Die Kölner Mietspanne beträgt **das Dreifache**: Neuehrenfeld 20,90 €/m²
  gegen Chorweiler 7,00 €/m². Auf 70 m² sind das 1.463 € gegen 490 € im Monat.
- **Kleine Wohnungen kosten je m² fast doppelt so viel**: unter 30 m² sind es
  23,60 €, bei 60 bis 79 m² nur 13,30 € — und Letztere sind mit 28,3 % die
  häufigste Angebotsgröße. Oberhalb von 40 m² ist der Quadratmeterpreis
  bemerkenswert stabil (13,30 bis 14,60 €).
- **Die teuerste Mietlage rentiert am besten.** Neuehrenfeld: 17,5
  Jahresmieten, 5,72 % brutto. Chorweiler: 32,1 Jahresmieten, 3,11 %. Faktor
  1,84 zugunsten der teuren Lage — weil dort die Miete hoch ist, der Kaufpreis
  aber vergleichsweise moderat. „Günstig kaufen" ist in Köln keine
  Renditestrategie.
- **Drei von neun Stadtbezirken schrumpfen** bis 2035: Lindenthal −2,0 %,
  Porz −0,9 %, Innenstadt −0,6 %. Rodenkirchen wächst um 8,6 % und trägt damit
  **9.600 der 12.200 zusätzlichen Einwohner** — knapp vier Fünftel des
  gesamten Wachstums. Ursache ist die Parkstadt Süd (über 3.000 Wohneinheiten
  ab 2030, rund 8.500 Erstbezieher); Raderberg verdoppelt dadurch seine
  Bevölkerung.
- **Wachstum und Preisniveau hängen nicht zusammen** (r = 0,00 über die neun
  Stadtbezirke). Die beiden teuersten Bezirke sind genau die, die schrumpfen —
  wo alles bebaut ist, kann niemand zusätzlich einziehen.
- **Möbliert vermieten hat sich verfünffacht**: Anteil 3 % (2015) auf 15 %
  (2025), Preisabstand von 16 % auf 35 %. Die Statistik warnt selbst davor,
  das als reinen Möblierungszuschlag zu lesen — dieser Vorbehalt steht auch
  auf der Seite.

**Eine Zahl wurde verworfen.** Eine frühere Recherche hatte für den amtlichen
Mietspiegel rund 11,50 €/m² ergeben. Dieser Wert liess sich an der Primärquelle
nicht belegen und steht deshalb nirgends auf der Seite. Der Kölner Mietspiegel
2025 ist ein *einfacher* Mietspiegel nach § 558c BGB und weist Tabellenwerte
nach Baualter, Grösse und Ausstattung aus, keinen einzelnen Durchschnitt.

### Startseite

Der Teaser nannte den Bericht, aber nichts von seinem Inhalt. Neu sind die
aktualisierten Kennzahlen (14,70 €, Faktor 26,3, +1,1 % bis 2035) und eine
**Liste von sechs Kapitelverweisen**, die direkt in die Ankerpunkte des
Berichts springen.

### Erstes Bild auf dem Marktbericht

Das Prüfwerkzeug hatte fehlende Bilder als grössten einzelnen Mangel gemeldet.
Gewählt ist ein Luftbild der **Neustadt/Süd** — nicht irgendein Kölnmotiv,
sondern der Stadtteil mit den meisten ausgewerteten Mietangeboten (529), der
im Miet- und im Renditekapitel mit eigenen Zahlen vorkommt. Die
Bildunterschrift stellt diesen Bezug her.
Achim Stump, CC BY-SA 4.0, über Wikimedia Commons.

### Zwei Zugänglichkeitsfehler auf der Startseite behoben

Beide bestanden schon vorher und fielen bei der Prüfung auf: Der Verweis aufs
Google-Unternehmensprofil und die verlinkten Vertrauenskarten hoben sich
**allein durch ihre Farbe** vom umgebenden Text ab (Kontrast 2,1:1 gegen
geforderte 3:1). Wer Farben schlecht unterscheidet, konnte sie nicht als Links
erkennen — Verstoss gegen WCAG 1.4.1. Beide sind jetzt unterstrichen.
Lighthouse-Zugänglichkeit der Startseite: 97 → **100**.

**Eine Falle beim Diagramm.** Die Beschriftung des Korridorbands („ab 40 m²:
13,30–14,60 €") stand zunächst auf Höhe des Bandes — also genau auf dem Wert
„13,30 €" des dritten Balkens, denn dieser Balken endet an der Bandunterkante.
Im Stylesheet ist das nicht zu sehen; erst der Blick auf die gerenderte Seite
zeigte die Überlappung. Die Beschriftung sitzt jetzt im freien Feld oben rechts,
verbunden durch eine gestrichelte Führungslinie.

**Geprüft:** Lighthouse mobil 100/100/100/100 auf dem Marktbericht,
Zugänglichkeit 100 auf der Startseite. Kein seitlicher Überlauf. Tabellen
brechen unter 700 px zu Blöcken um. Eigenwiederholung des Berichts 0,0 %,
nächstverwandte Seite nur 25 %.

**Cache-Buster:** `styles.css?v=67` auf allen 231 Seiten (`main.js` unverändert
bei v=34).

## Was in v54 umgesetzt wurde

### Immobilienmarktbericht Köln 2026

Neue Seite unter `immobilienmarktbericht-koeln-2026.html`, 2.100 Wörter mit
259 Zahlen. Grundlage war eine Textvorlage samt SEO-Vorgaben; alle darin
genannten Zahlen wurden geprüft, soweit möglich nachgerechnet — mit drei
Ergebnissen, die von der Vorlage abweichen.

**Bodenrichtwerte selbst ausgewertet.** Statt eine Zahl zu übernehmen, sind
die BORIS-Rohdaten (Stichtag 1.1.2026) direkt ausgewertet: 387 Kölner
Wohnbauzonen, Median **870 Euro**, Spanne 370 bis 3.100 Euro. Die Vorlage
nannte 930 Euro und 240 bis 3.550 Euro — die Obergrenze erscheint erst mit
Mischgebieten, die Untergrenze ließ sich gar nicht reproduzieren. Auf der
Seite stehen die nachgerechneten Werte mit ausgewiesener Abgrenzung.

**Ein Faktenfehler korrigiert.** Die Vorlage nannte 2024 den „niedrigsten Wert
seit Beginn der Erhebung 2015". Die Bautätigkeitsstatistik der Stadt Köln
(Kölner Statistische Nachrichten 11/2025) zeigt: 1990 lag der Wert mit 1.628
Wohnungen noch niedriger. Richtig ist der Rückgang um **48,5 Prozent**
gegenüber dem Vorjahr.

**Die stärkste Zahl kam aus der eigenen Recherche.** Der Bauüberhang liegt bei
**10.308 genehmigten, aber nicht fertiggestellten Wohnungen** — historischer
Höchststand. Davon sind **57 Prozent noch nicht einmal im Bau**. Genehmigungen
sind also nicht der Engpass; es fehlt die Umsetzung. Diese Zahl stand in
keiner Vorlage.

**Ein Widerspruch zur eigenen Website aufgelöst.** Die Vorlage nannte für
Lindenthal 6.000 bis 6.500 Euro je Quadratmeter — Angebotspreise aus Portalen.
Unsere Lindenthal-Seite nennt 5.569 Euro aus 144 beurkundeten Kaufverträgen.
Beides stimmt, misst aber Verschiedenes. Statt den Widerspruch stehenzulassen,
macht die Seite ihn zum Thema: Der Abstand von zwölf Prozent zwischen Wunsch
und Abschluss ist selbst die Nachricht.

**Alle 85 Stadtteile als Tabelle.** Aus denselben Rohdaten je Stadtteil
zusammengefasst — Median, Spanne, Zonenzahl. Zwischen Bayenthal (2.830 €) und
Godorf (460 €) liegt der Faktor 6,2. Für Eigentümer ist aber die Spaltenspanne
interessanter als die Rangfolge: In Müngersdorf entscheidet die Adresse über
mehr als das Doppelte, in Klettenberg über vier Prozent.

**Neubau gegen Bestand, selbst gerechnet:** In den acht Stadtteilen, für die
der Gutachterausschuss beide Werte ausweist, liegt Neubau bei 7.556 Euro je
Quadratmeter (316 Verträge), Bestand bei 4.934 Euro (751 Verträge) — ein
Aufschlag von 53 Prozent.

Das Schema folgt der Person-Autorschaft der übrigen Seiten statt der in der
Vorlage genannten Organization; die dort angegebenen www-Adressen leiten weiter,
und die genannte `logo.png` existiert nicht. Teaser auf der Startseite, Eintrag
in Sitemap und Navigation, Weiterleitungen vom geplanten Slug.

Nicht übernommen: „rund 750 Bankpartner" (unbelegt, § 5a UWG). Die Angabe
steht allerdings weiterhin im Navigationsmenü und damit auf allen 231 Seiten.

Lighthouse mobil 100/100/100/100.

Cache-Buster: `styles.css?v=66` und `main.js?v=34`.

## Was in v53 umgesetzt wurde

### Veedelseite Köln-Klettenberg

Sechste ausgebaute Stadtteilseite, von 571 auf 1.629 Wörter. Der Aufhänger
steht in der Textvorlage und ließ sich mit den amtlichen Daten belegen: Der
Gutachterausschuss wertete für 2025 in Klettenberg 49 Wohnungsverkäufe aus.
Der Durchschnitt lag bei 5.339 Euro je Quadratmeter — **tatsächlich gezahlt
wurden zwischen 2.858 und 8.459 Euro.** Das Dreifache.

Die eigentliche Erkenntnis entsteht erst im Vergleich dreier Faktoren:

| | Spanne | Faktor |
|---|---|---|
| Bodenrichtwertzonen | 1.590 – 1.650 €/m² Grundstück | **1,04×** |
| Baujahrsgruppen | 5.257 – 5.770 €/m² Wohnfläche | **1,10×** |
| tatsächlich gezahlt | 2.858 – 8.459 €/m² Wohnfläche | **2,96×** |

**Weder die Lage noch das Baujahr erklären die Spreizung.** Klettenberg hat
nach Marienburg den homogensten Boden aller zwanzig ausgewerteten Kölner
Stadtteile — nur zwei Zonen, die sich um vier Prozent unterscheiden. Was den
Preis macht, ist das einzelne Objekt. Das ist das genaue Gegenstück zur
Lindenthaler Seite, wo die Adresse entscheidet.

Gestalterisch trägt der Kopf diese Aussage: eine Preisskala von 2.858 bis
8.459 Euro, auf der der Durchschnitt an seiner echten Position sitzt — bei
44 Prozent der Strecke, nicht in der Mitte. Erste Seite der Reihe in Grün;
die fünf davor arbeiten mit Navy und Sandton.

Dazu kommen die Baujahrsgruppen, die Häuserzahlen mit ihren kleinen
Fallzahlen (vier beziehungsweise drei Verkäufe — ausdrücklich als solche
gekennzeichnet), die Denkmal-AfA nach § 7i und § 10f EStG, und ein Abschnitt
über die Unterlagen, die eine Bank vor der Finanzierungszusage sehen will.

**Zwei Fallen bei dieser Seite:**

- **`.replace(",", ".")` auf einem ganzen Textblock.** Gedacht war die
  Eindeutschung der Tausendertrennzeichen aus der f-String-Formatierung —
  getroffen hat es jedes Satzkomma: „bei einem Stadtteil. dessen Boden".
  Sichtbar nur im Browser. Jetzt formatiert eine eigene Funktion die Zahlen.
- **Vereinfachungstoleranz je Stadtteilgröße neu justieren.** Klettenberg ist
  mit 1,2 km² deutlich kleiner als die bisherigen Veedel. Auf dem engen
  Ausschnitt reduzierte die von Lindenthal übernommene Toleranz kleine Häuser
  auf zwei Punkte — von 1.758 Gebäuden im Bild wurden nur 838 gezeichnet, die
  Karte wirkte halbleer.

Die dritte Kartenansicht nach Bodenwert je Quadratmeter Wohnfläche entfällt
hier bewusst: Bei zwei Zonen mit vier Prozent Abstand bringt die Umrechnung
keinen Erkenntnisgewinn.

Lighthouse mobil 100/100/100/100.

Cache-Buster: `styles.css?v=62` und `main.js?v=34`.

## Was in v51 umgesetzt wurde

### Lindenthal überarbeitet — der Kopf war live unlesbar

Rückmeldung nach der Veröffentlichung: „sieht nicht gut aus, viele Fehler,
zu kurz." Alle drei Punkte trafen zu.

**Der Kopf war kaputt.** `.page-hero:not(.page-hero--img)` legt einen radialen
Blauverlauf über jeden Seitenkopf und ist mit zwei Klassen spezifischer als
`.lind-kopf`. Der helle Sandton kam deshalb nie an: Auf der Live-Seite stand
dunkelbrauner Text auf dunkelblauem Grund. Dasselbe traf jeden Absatz im Kopf
— `.page-hero p` färbte die große Zahl blaugrau und schrumpfte sie von 34 auf
19 Pixel.

Der Fehler war **nur im Browser sichtbar**, nicht im Stylesheet und nicht in
den Messwerten. Beim Bauen hatte ich den Handy-Screenshot des Rechners
geprüft, aber nie den Kopf am Rechner. Sämtliche Kopfregeln tragen jetzt
`.page-hero` als Präfix.

**Die Seite war zu kurz.** Mit 1.516 Wörtern die kürzeste der fünf
Veedelseiten, Deutz hat 2.767. Drei Abschnitte kamen dazu:

- **Zonen Straße für Straße.** Die acht Straßen aus der Textvorlage wurden
  über Nominatim-Koordinaten und einen Punkt-in-Polygon-Test ihren amtlichen
  Bodenrichtwertzonen zugeordnet. Ergebnis: Stadtwaldgürtel und
  Karl-Schwering-Platz liegen in derselben Zone, Bachemer und Theresienstraße
  ebenfalls — zwischen der günstigsten und teuersten Adresse liegen 1.300 Euro
  je Quadratmeter.
- **Fünf Objektarten** mit ihren jeweiligen Bewertungswegen: Villa, Haus,
  Eigentumswohnung, Grundstück, Mehrfamilienhaus.
- **Der Verkaufsablauf** in neun Schritten.

Jetzt 2.478 Wörter — nach Deutz die zweitlängste Veedelseite.

### Ein Datenfund in BORIS NRW

Bei der Zuordnung der Straßen fiel auf, dass zwei Zonen dieselbe
Umringgeometrie tragen. Nachgeprüft **direkt im Shapefile**: Es ist kein
Lesefehler, die Records 12001 und 12002 haben tatsächlich identische
Geometrien bei verschiedenen Werten, Lagebezeichnungen und
Richtwertgrundstücken. Betroffen sind in Lindenthal drei Flächenpaare, in
Ehrenfeld fünf und in Sülz zwei.

Übereinandergezeichnet verdeckt eine Zone die andere, und die Karte behauptet
etwas Falsches. Sie zeichnet solche Flächen jetzt **einmal** und nennt beim
Antippen beide Werte mit dem Hinweis, dass die amtlichen Umringe hier
deckungsgleich abgelegt sind. Aus zwölf übereinanderliegenden Zonen wurden
neun saubere Flächen.

### Weitere Korrekturen

- Überschrift bricht kontrolliert um statt „Sie" allein in eine Zeile zu
  setzen.
- Der Hinweis „bei Eigentumswohnungen Ihr Anteil" steht unter dem Eingabefeld
  statt im Label — dort drückte er das Feld aus der Reihe.
- `line-height` der Kopf-Unterzeile gesetzt; sie erbte die .95 der großen Zahl
  und klebte beim Umbruch zusammen.

Kontraste am gerenderten Bild gemessen: schlechtester Wert 4,99:1.
Lighthouse mobil 100/100/100/100.

Cache-Buster: `styles.css?v=55` und `main.js?v=33`.

## Was in v50 umgesetzt wurde

### Veedelseite Köln-Lindenthal

Fünfte ausgebaute Stadtteilseite, von 648 auf 1.512 Wörter. Der Aufhänger ist
das genaue Gegenstück zu Ehrenfeld: **Lindenthal hat mit 2.120 Euro je
Quadratmeter den zweithöchsten Bodenrichtwert der zwanzig ausgewerteten
Kölner Stadtteile — beim Preis für eine weiterverkaufte Wohnung aber nur
Rang 4.** In Ehrenfeld ist es umgekehrt.

Die Erklärung steht in den amtlichen Daten: Die Geschossflächenzahl liegt in
Lindenthal zwischen 0,8 und 2,0, in Ehrenfeld reicht sie bis 2,8. Wo locker
gebaut werden darf, trägt weniger Wohnfläche denselben Boden.

**Blickfang ist ein Bodenanteil-Rechner.** Er beantwortet, welcher Teil des
Werts im Grundstück steckt — die Frage, die in einem Villenveedel über die
Verkaufsstrategie entscheidet. Steckt der Wert im Gebäude, zahlt sich eine
Modernisierung aus; steckt er im Boden, kaufen Interessenten die Lage. Der
Rechner deckelt seine Prozentangabe **nicht** bei hundert: Wenn der Bodenwert
den Vergleichswert übersteigt, ist genau das die Aussage.

Die Karte hat eine dritte Ansicht, die es auf keiner anderen Seite gibt: Sie
färbt die Bodenrichtwertzonen nicht nach ihrem Wert je Quadratmeter
Grundstück, sondern **je Quadratmeter Wohnfläche**. Dabei dreht sich die
Rangfolge — die Zone an der Werthmannstraße hat mit 1.220 Euro den
*niedrigsten* Bodenrichtwert Lindenthals, wegen einer Geschossflächenzahl von
0,8 aber mit rund 1.525 Euro fast den *höchsten* Anteil je Quadratmeter
Wohnfläche.

Erster heller Kopf der Reihe. Die vier Seiten davor arbeiten alle mit dunkler
Fläche; Lindenthal bekommt Sandton, und das Foto folgt als eigenes Band unter
dem Text statt dahinter — der Kontrast lässt sich so vorab bestimmen, statt
ihn am gerenderten Bild nachmessen zu müssen.

### Selbstwiederholung auf den 55 Umlandseiten entfernt

Gemessen wiederholte jede dieser Seiten **rund 13 Prozent ihres eigenen
Textes**: Lage- und Bebauungsbeschreibung standen einmal im Kopfabschnitt und
ein zweites Mal weiter unten zwischen den Marktdaten. Entfernt wurden 4.673
Wörter, im Schnitt 136 je Seite. Die Eigenwiederholung sank damit von 13,0 auf
**0,0 Prozent** — auf keiner der 55 Seiten steht noch ein Satz zweimal.

**Was nicht funktioniert hat, und warum es hier steht:** Der erste Anlauf
wollte die dreizehn Sätze ersetzen, die auf allen 55 Seiten wortgleich stehen
— durch Sätze, die je Stadt gerechnete Zahlen tragen. Das Ergebnis war eine
*höhere* gemessene Ähnlichkeit (77 → 79 Prozent), nicht eine niedrigere. Der
Grund ist im Nachhinein offensichtlich: Die Ersatzsätze behielten denselben
Satzbau und tauschten nur Ziffern, und das Prüfwerkzeug misst Wortketten. Ein
zusätzlicher Zahlenabschnitt hatte denselben Effekt. Beide Änderungen sind
zurückgenommen worden.

Die Ähnlichkeit *zwischen* den Umlandseiten liegt weiter bei rund 79 Prozent.
Sie lässt sich mit Textkosmetik nicht lösen — 55 Seiten, die dasselbe
Angebot für verschiedene Orte beschreiben, ähneln sich zwangsläufig. Wer sie
wirklich unterscheiden will, braucht je Ort eigene Inhalte: eigene Fotos,
eigene Verkaufsfälle, eigene Marktbeobachtungen. Das ist eine inhaltliche
Aufgabe, keine technische.

Lighthouse mobil auf Lindenthal und den Umlandseiten 100/100/100/100.

Cache-Buster: `styles.css?v=54` und `main.js?v=32`.

## Was in v49 umgesetzt wurde

### Veedelseite Köln-Ehrenfeld

Vierte ausgebaute Stadtteilseite, von 754 auf 2.018 Wörter. Der Aufhänger
kommt aus den Daten, nicht aus einer Textvorlage: **In Ehrenfeld wurden 2025
mehr Neubau- als Bestandswohnungen verkauft** — 141 gegen 112 Verträge. Das
ist in keinem der zwanzig ausgewerteten Kölner Stadtteile sonst so. Der Kopf
der Seite stellt beide Zahlen als Waage gegenüber.

Für Verkäufer ist der Preisabstand das Argument: Neubau kostete 7.149 Euro je
Quadratmeter, Bestand 5.078 — ein Aufschlag von 41 Prozent. Für dieselbe
Summe bekommt ein Käufer im Bestand rund 40 Prozent mehr Fläche. Damit wird
aus der gefürchteten Neubaukonkurrenz ein Vergleichsmaßstab, der den eigenen
Preis erklärt.

**Der Blickfang: ein Satzungsprüfer.** Seit dem 24. Januar 2024 gilt in
Ehrenfeld-Ost eine Soziale Erhaltungssatzung. Innerhalb des Gebiets brauchen
Rückbau, Änderung und Nutzungsänderung eine zusätzliche Genehmigung der Stadt
— auch dort, wo die Landesbauordnung keine verlangt. Die Seite beantwortet,
ob eine Lage betroffen ist, geprüft gegen die **amtliche Gebietsgeometrie aus
dem Geoportal der Stadt Köln** (Gebiet E31). Zuerst hatte ich nur die vier im
Satzungstext genannten Grenzstraßen gezeichnet; die laufen aber weit über das
Gebiet hinaus und ließen die Satzung größer wirken, als sie ist. Bei einer
Genehmigungspflicht ist das nicht hinnehmbar. Die Abfrage bleibt ausdrücklich
eine Orientierung — verbindlich ist allein die Auskunft der Stadt.

Aus der Prüfung fiel ein Befund ab, der nirgends steht: **Die vier höchsten
Bodenrichtwerte Ehrenfelds liegen sämtlich im Satzungsgebiet, die vier
niedrigeren außerhalb.** Ausgerechnet dort, wo der Boden am meisten wert ist,
sind bauliche Veränderungen genehmigungspflichtig.

Ein zweiter Widerspruch wird auf der Seite aufgelöst: Ehrenfeld liegt beim
Bodenrichtwert auf Rang 13, beim Wohnungspreis auf Rang 7. Billiger Boden,
teure Wohnungen — die Erklärung sind Geschossflächenzahlen von 2,3 bis 2,8.
Wo hoch gebaut wird, verteilt sich der Bodenanteil auf viele Wohnungen.

### Alle Veedelkarten und Diagramme telefontauglich

Deutz, Sülz und Zollstock hielten ihre Karten auf der Entwurfsbreite fest
(`min-width: 820px`) und machten den Rahmen seitlich beweglich. **Am Gerät
gemessen sah man davon 44 Prozent**, der Hinweis „seitlich scrollbar"
verschwand hinter dem Kopfbereich, und niemand erfuhr, was fehlt.

Grund für die feste Breite waren die Namen an den Kartenpunkten: bei voller
Skalierung schrumpft „Bahnhof Köln-Ehrenfeld" auf knapp fünf Pixel. Die
Lösung: **Die Punkte tragen Ziffern, die Namen stehen als Liste darunter.**
Eine Ziffer im Kreis bleibt lesbar, ein Straßenname nicht. Auf dem Telefon
ist die Liste zugleich das bequemere Bedienelement — ein 44 Pixel hoher Knopf
trifft sich sicherer als ein Kartenpunkt.

Dasselbe für die drei Verlaufsdiagramme (vorher 560 Pixel fest): Sie werden
jetzt mit größerer Grundschrift und breiteren Rändern gezeichnet und
skalieren mit.

Die vier Datentabellen auf der Deutzer Seite brechen auf schmalen Fenstern zu
Blöcken um. Vorher hatte dort eine Tabellenzeile **187 Pixel Höhe**, weil die
letzte Spalte mit ihrem Erklärtext außerhalb des Sichtbereichs lag und die
Zeile auseinanderzog — sichtbar waren vor allem leere Flächen.

### Fallen bei diesem Stand

- **Das erste `<svg>` einer Seite ist das Telefon-Icon im Kopfbereich.** Der
  erste Anlauf des Einsetzskripts ersetzte genau dieses Icon und ließ die
  Karte stehen. Jetzt wird gezielt nach der Kartenklasse gesucht, und ein
  Fund unter 50.000 Zeichen gilt als Fehlgriff.
- **`.dz-ring` war früher ein unsichtbarer Halo** (`opacity: 0`), der erst
  bei Hover erschien; den sichtbaren Punkt trug ein dritter Kreis. Nach dem
  Umbau trug der Ring die Ziffer — und war unsichtbar.
- **`role="button"` auf einem `<li>`** nimmt der Liste ihre `listitem`-Kinder.
  Lighthouse meldet das als fehlerhaften Accessibility-Baum. Ein echtes
  `<button>` im `<li>` löst das und bringt die Tastaturbedienung mit.
- **Das sichtbare Zeichen gehört ins `aria-label`.** Steht dort nur der Name,
  findet die Sprachsteuerung den Punkt nicht, den der Nutzer benennt („Klick
  auf 1").
- **Kartenpunkte nie aus einer Bounding Box ableiten.** Leo-Amann-Park und
  Gewerbeband lagen 100 beziehungsweise 180 Meter daneben, weil ich das
  Minimum statt des Flächenschwerpunkts genommen hatte.
- **`.page-hero p` schlägt eine einfache Klasse.** Der Ehrenfelder Lead war
  blaugrau statt weiß, bis die Regel spezifischer wurde.

Lighthouse mobil auf allen vier Veedelseiten 100/100/100/100.

Cache-Buster: `styles.css?v=52` und `main.js?v=31`.

## Was in v48 umgesetzt wurde

### Autorschaft und Aktualität — für Google und für KI-Antworten

Anlass war eine Sichtbarkeitsanalyse. Der Befund: `author` und
`datePublished` kamen auf **null von 230 Seiten** vor. Baris stand zwar auf
jeder Seite, aber nirgends maschinenlesbar als Fachautor mit Qualifikation.

Das ist deshalb wichtig, weil bis Ende 2026 rund 60 Prozent der kommerziellen
Suchanfragen von KI-Antworten beeinflusst sind. Diese Systeme zitieren
bevorzugt Inhalte mit erkennbarem Autor und nachvollziehbarem Stand — genau
wie Googles E-E-A-T-Bewertung.

**Was jetzt auf 223 Seiten steht** (Rechtstexte, Rechner und das interne
Cockpit bleiben außen vor, dort sagt eine Autorschaft nichts aus):

- **Person-Schema** mit fester `@id`, das die belegbaren Qualifikationen
  trägt: Erlaubnis nach § 34c GewO (Stadt Köln) und § 34i GewO (IHK zu Köln),
  Tätigkeitsschwerpunkte, Anschrift, persönliche Profile. Ausschließlich
  Angaben aus dem Impressum — nichts Ausgedachtes, keine Berufsjahre, keine
  Fallzahlen.
- **WebPage-Schema** je Seite mit `author`-Verweis auf diese `@id` und
  `dateModified` aus der Sitemap.
- **Sichtbare Autorenzeile** vor dem Schlussaufruf: Foto, Name, Funktion,
  beide Erlaubnisse und der Stand. Sichtbar, weil Google wie auch die
  KI-Systeme den gerenderten Text auswerten und nicht nur das Schema.

**Entitäten zusammengeführt.** Die 205 bestehenden `RealEstateAgent`-Schemas
hatten keine `@id`. Ohne gemeinsame Kennung liest Google zwei getrennte Firmen,
und die Verknüpfung „Baris ist Inhaber dieser Firma" geht ins Leere. Jetzt
teilen sich alle dieselbe `@id`, und `founder`/`worksFor` verbinden Person und
Betrieb in beide Richtungen. Genau diese Verknüpfung werten KI-Systeme aus.

**Zwei Fallen dabei:**

- Der Sitemap-Parser machte aus `https://high-seller.de/` den Hostnamen statt
  `index.html` — ausgerechnet die Startseite blieb zunächst ohne Autorschaft.
- Die Schema-URL kommt jetzt aus dem `canonical`, nicht aus dem Dateinamen.
  Für die Startseite hätte sonst `/index.html` im Schema gestanden, während
  `canonical` auf `/` zeigt: ein Widerspruch, der auf die weiterleitende
  Adresse verweist.

**Pflege: `tools/autorschaft-pflegen.py`.** Das Skript setzt die Autorschaft
auf neuen Seiten und zieht auf bestehenden das Datum nach — sichtbar und im
Schema gleichzeitig. **Nach jeder Seitenüberarbeitung laufen lassen**, sobald
die Sitemap aktualisiert ist. Ein stehen gebliebenes „zuletzt geprüft am" wäre
schlimmer als gar keine Angabe.

Lighthouse mobil unverändert 100/100/100/100.

Cache-Buster: `styles.css?v=46` und `main.js?v=28` auf allen Seiten.

## Was in v47 umgesetzt wurde

### Köln-Zollstock als dritte ausgebaute Veedelseite

Wieder ein eigenes Gesicht — und diesmal liefert Baris' Vorlage selbst den
Blickfang. In seinen zwölf WhatsApp-Texten steckt eine Beobachtung, die auf
keiner Maklerseite steht: **Die Preisquellen widersprechen sich massiv.**

| Quelle | Wohnung Zollstock | Grundlage |
|---|---|---|
| Gutachterausschuss Köln | 4.368 €/m² | 114 notarielle Kaufverträge |
| ImmoScout24, Q2 2026 | 4.756 €/m² | Angebotspreise |
| Engel & Völkers, Q2 2026 | 5.700 €/m² | Angebotspreise |

1.332 € Unterschied je Quadratmeter. Der Grund ist der Kern der Sache:
**Portale messen Angebote, der Gutachterausschuss misst Abschlüsse.** Deshalb
ist der amtliche Wert der niedrigste — und der einzige, der auf tatsächlich
bezahlten Preisen beruht. Bei Häusern kehrt sich das Verhältnis sogar um.

**Der Blickfang ist ein Rechner, der das begreifbar macht.** Objektart wählen,
Quadratmeter eintragen, und die Seite zeigt alle Quellen nebeneinander mit
Balken plus die Spanne in Euro: Bei 80 m² sind das **106.560 €** Unterschied
zwischen niedrigster und höchster Einschätzung. Genau Baris' Botschaft, nur
nicht behauptet, sondern vorgerechnet.

**Zweiter nischiger Block: Denkmalschutz und Denkmal-AfA.** Zollstock hat
Häuser von um 1900 am Höninger Weg und genossenschaftlichen Siedlungsbau der
1920er und 1950er, teils von Wilhelm Riphahn; ein Quartier heißt bis heute
Schutzmannshausen. Die Seite nennt die Abschreibung konkret — § 7i EStG für
vermietete Objekte (12 Jahre, 8×9 % + 4×7 %), § 10f EStG für selbstgenutzte
(10 Jahre × 9 %) — samt dem häufigsten Irrtum: **Die Prozentsätze gelten nicht
für den Kaufpreis, sondern nur für bescheinigte Sanierungskosten.** Mit dem
Hinweis, dass Maßnahmen vorab mit der Denkmalbehörde abzustimmen sind und die
steuerliche Bewertung zum Steuerberater gehört.

**Eigenes Seitengesicht:** Panoramaband oben (Luftbild Südstadion), darunter
dunkle Fläche mit Titel und den drei widersprechenden Zahlen. Deutz hat einen
Vollbild-Bildkopf, Sülz einen geteilten — Zollstock das Band.

**Ein Fund beim Zusammenführen der BORIS-Jahrgänge**, der auch für die anderen
Seiten gilt: Eine Fläche am Höninger Weg wurde bis 2024 als Wohnzone
Irmgardstraße geführt (1.060 € je m²), taucht im Jahrgang 2025 aber als eigene
**Gewerbezone mit 205 €** auf. Wer nur die Zahlen vergleicht, liest daraus
achtzig Prozent Wertverlust — tatsächlich wurde die Zone neu zugeschnitten und
anders eingestuft. Die Verlaufskurve zeigt deshalb nur, was durchgängig
Wohnbauland war, und die Seite erklärt die Falle. **Vor jeder
Bodenrichtwert-Zeitreihe die Nutzungsart mitprüfen.**

Zollstock ist außerdem der Gegenpol zu Sülz: 338 neue Wohnungen in einem Jahr
(2,4 % des Bestands, Rang drei aller ausgewerteten Stadtteile) gegenüber 0,18 %
in Sülz. Wer hier verkauft, hat echte Neubaukonkurrenz.

**Aus der Vorlage nicht übernommen:** die unbelegte Zahl „über 750 Banken"
(§ 5a UWG, steht weiter unten als offener Punkt) und die Aussage, Vor-Ort-
Termine hätten zu höheren Verkaufspreisen geführt.

**Achtung, in Baris' Vorlage stand eine tote Adresse:** Er nennt dort
`B.oelmez@highseller-immobilien.koeln` — die Domain wurde am 31.07.2026
aufgegeben (siehe v41). Die Seite verwendet die regulären Kontaktwege.
Wo diese Adresse sonst noch kursiert, sollte sie ersetzt werden.

**Zwei Fallen dieser Runde:** `display:grid` schlägt das `hidden`-Attribut —
die ausgeblendeten Objektart-Zeilen des Rechners blieben sichtbar, bis
`.quelle[hidden]{display:none}` ergänzt war. Und die Mindestfläche aus dem
Sülz-Skript filterte Zollstocks kleinteiligen Siedlungsbau weg: statt 4.089 nur
1.191 Gebäude. Pro Stadtteil neu justieren.

Lighthouse mobil 100/100/100/100 — die Denkmalkarten hatten zunächst `h4` unter
`h2` und rissen ein Loch in die Gliederung.

Cache-Buster: `styles.css?v=45` und `main.js?v=27` auf allen Seiten.

## Was in v46 umgesetzt wurde

### Bodenrichtwerte über fünfzehn Jahre — auf beiden Veedelseiten

Phillip wollte auf Deutz und Sülz je etwas ergänzen, das nischig ist und sich
nicht ergoogeln lässt. Das hier ist es: **BORIS NRW veröffentlicht die
amtlichen Bodenrichtwerte seit 2011, aber immer nur als Momentaufnahme eines
Jahres. Was aus einer einzelnen Zone über die Zeit geworden ist, steht
nirgends.** Sechzehn Jahrgänge nebeneinandergelegt ergeben eine Zeitreihe, die
es so im Netz nicht gibt.

**Das Ergebnis ist eine unbequeme Nachricht.** Mittelwert der Wohnbauzonen:

| | 2011 | 2019 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|
| Deutz | 585 € | 1.135 € | **1.745 €** | 1.525 € | 1.410 € | 1.420 € |
| Sülz | 695 € | 1.440 € | **2.160 €** | 1.845 € | 1.740 € | 1.740 € |

Bis 2023 hat sich der Bodenwert in beiden Stadtteilen etwa verdreifacht, seit
dem Höchststand ging es um **19 % zurück** — in Deutz und Sülz fast auf den
Prozentpunkt gleich. Der Knick kam mit dem Jahrgang 2024. Seit 2025 ist die
Kurve flach: Sülz unverändert 1.740 €, Deutz plus zehn Euro.

Für die Beratung ist genau das der Wert dieser Auswertung. Die häufigste
Eigentümerfrage lautet „soll ich noch warten?" — und die Kurve beantwortet sie
ehrlich: Der Höchststand ist zwei Jahre her, aber ein weiterer Rückgang ist
seit einem Jahr nicht mehr zu sehen.

**Ein Lesehinweis, den fast alle übersehen** und der deshalb auf beiden Seiten
steht: Bodenrichtwerte gelten zum Stichtag 1. Januar und bilden das jeweils
abgelaufene Jahr ab. Der im Jahrgang 2024 sichtbare Einbruch ist also am Markt
2023 passiert, kurz nach der Zinswende. Wer amtliche Werte mit tagesaktuellen
Angebotspreisen vergleicht, vergleicht zwei verschiedene Zeitpunkte.

**Sülz hat einen Ausreißer**, der die Kernbotschaft der Seite stützt: Am Platz
der Kinderrechte stieg der Wert zuletzt von 1.950 € auf 2.610 €, während alle
anderen Zonen nachgaben. „Der Markt" ist nicht einmal innerhalb eines
Stadtteils eine einzige Zahl.

**Zuordnung über den Ort, nicht über die Zonennummer.** Zonen werden
gelegentlich neu geschnitten und umnummeriert; ein Abgleich über `BRWZNR`
liefert stille Fehltreffer. `brw-verlauf-lesen.py` bestimmt stattdessen für
jede aktuelle Zone einen Punkt im Inneren und sucht im alten Jahrgang das
Polygon, das ihn enthält (Strahlverfahren).

Die Kurve zeichnet sich beim Sichtbarwerden. Die Pfadlänge wird dafür zur
Laufzeit über `getTotalLength()` gemessen — ein fester Wert im Stylesheet
passte bei anderer Kurvenform nicht.

Beide Textblöcke sind eigenständig geschrieben, nicht gespiegelt: Deutz führt
über den Verkaufszeitpunkt, Sülz über die drei Lesarten der Kurve.

Cache-Buster: `styles.css?v=44` und `main.js?v=26` auf allen Seiten.

## Was in v45 umgesetzt wurde

### Sülz: neuer Bildkopf und eine Karte, die mitfährt

Phillip war mit der ersten Sülz-Fassung nicht zufrieden: Das Design gefiel
nicht, der Text ging unter, und der Blickfang war zu leise. Beides ist
überarbeitet.

**Geteilter Bildkopf statt Text über Foto.** Vorher stand der Text auf dem
hellen Beethovenpark-Bild. Der Kontrast war messbar in Ordnung, optisch ging
er trotzdem unter — **ein Foto ist nie eine ruhige Textfläche**, egal wie gut
der Verlauf liegt. Jetzt liegt der Text auf einer eigenen dunklen Hälfte, das
Bild daneben, mit weicher Kante dazwischen. Der Kopf nimmt volle Bildschirm-
höhe statt 42 %, die Überschrift trägt die Kernaussage („Hier wird kaum
gebaut. Aber viel gehandelt."), darunter ein überlappendes Zahlenband, dessen
Ziffern beim Sichtbarwerden hochlaufen.

**Die Karte erzählt jetzt.** Beim Scrollen bleibt sie stehen, während der Text
daneben durchläuft; jeder Abschnitt hebt eine andere Bodenrichtwertzone hervor
und die Kamera fährt dorthin. Fünf Stationen führen vom Spitzenwert am Platz
der Kinderrechte (2.610 €) über die solide Mitte und das Kerngebiet an der
Sülzburgstraße bis zum unteren Rand an der Mayener Straße (1.430 €) und zum
Gewerbegebiet (475 €). So sieht man die Preisspanne entstehen, statt sie
erklärt zu bekommen.

Drei Dinge, die dabei zu lernen waren:

- **Die viewBox lässt sich nicht per CSS überblenden.** Sie wird Bild für Bild
  interpoliert; `getBBox()` liefert die Zonenausdehnung im selben
  Koordinatensystem, in dem auch die viewBox rechnet.
- **Fester Ausschnitt statt zonenabhängigem Zoom.** Die zehn Zonen sind extrem
  verschieden groß; ein Faktor je Zone ergab Fahrten zwischen 1,0- und
  3,3-fach, was unruhig wirkte. Jetzt immer 1,92-fach, zentriert auf die
  Zonenmitte.
- **Der Erzählmodus muss die Zonenansicht einschalten.** Sonst hebt das
  Scrollytelling Flächen hervor, die gar nicht eingeblendet sind — genau das
  passierte im ersten Anlauf.

**Auf schmalen Bildschirmen kein Scrollytelling.** Eine feststehende Karte
fräße dort die halbe Anzeige. Stattdessen Karte oben, Schritte darunter, alle
Zonen normal eingefärbt. Ohne JavaScript oder bei reduzierter Bewegung gilt
dasselbe — es geht nur die Führung verloren, kein Inhalt.

**Und wieder die Gitterfalle:** `.szene__karte` brauchte `min-width:0`, sonst
bläht die Karte mit ihrer Mindestbreite die Zelle auf und schiebt den Inhalt
über den Rand. Dieselbe Ursache wie bei den Tabellen im Juli.

Lighthouse mobil weiterhin 100/100/100/100, kein horizontaler Überlauf bei
390 px, Seite mit 0 % Eigenwiederholung und 0 % Bausteinanteil.

Cache-Buster: `styles.css?v=43` und `main.js?v=25` auf allen Seiten.

## Was in v44 umgesetzt wurde

### Köln-Sülz als zweite ausgebaute Veedelseite

Zweite Seite des Vorhabens, und bewusst **anders gebaut als Deutz**. Nicht der
Abwechslung wegen: Die Stadtteile erzählen verschiedene Geschichten, und die
Seiten sollen das zeigen.

**Der Aufhänger steht in drei Zahlen.** In Sülz wird kaum gebaut, aber viel
gehandelt: 0,18 % Neubau gemessen am Bestand (40 Wohnungen auf 22.626,
drittniedrigster Wert der zwanzig ausgewerteten Stadtteile), dabei 121
notarielle Kaufverträge im Jahr (Rang vier). Bei Deutz war die Botschaft genau
umgekehrt — dort steht Neubaukonkurrenz im Vordergrund. Dritte Zahl: die
Bodenrichtwerte reichen von 1.430 € an der Mayener Straße bis 2.610 € am Platz
der Kinderrechte, fast Faktor zwei innerhalb eines Stadtteils.

**Eigene Bausteine statt Deutz-Baukasten:**
- **Heller Bildkopf** (Beethovenpark) statt des abgedunkelten Rheinbilds.
- **Dreisatz-Leiste** mit den drei tragenden Zahlen statt Kennzahlenkacheln.
- **Gegenüberstellung der zwei Käufergruppen** statt Objektartentabelle —
  Familien gegen Kapitalanleger und Elterngeneration, mit dem, was jede Gruppe
  anzieht, wofür sie zahlt, was sie stört und was ins Exposé gehört. Das ist
  in Sülz keine Marketingfigur: 61,4 % Einpersonenhaushalte (Universität)
  stehen drei Gymnasien und zwei Encke-Parks (Familien) gegenüber.
- **Bodenwertrechner an der Karte** — der eigentliche Blickfang, siehe unten.
- **Sechs Mikrolagenfragen** als nummerierte Liste statt Fehlerkarten.

### Bodenwertrechner: die Karte rechnet mit

Wer in der Zonenansicht eine Fläche antippt, bekommt den amtlichen
Bodenrichtwert übernommen, trägt seine Grundstücksfläche ein und sieht sofort
den rechnerischen Bodenwert. Der Rechner ist bis zur ersten Auswahl verborgen,
damit niemand vor einem leeren Formular steht.

Bewusst nur eine Multiplikation, mit deutlichem Hinweis darunter: Das Ergebnis
ist der Wert des **Bodens**, nicht der der Immobilie — bei einer
Eigentumswohnung entfällt davon nur der Miteigentumsanteil, bei einem Haus
kommt der Gebäudewert hinzu. Alles andere wäre eine Scheingenauigkeit, die
sich nicht halten lässt. Der Rechner liest den Wert aus dem `aria-label` der
Zone, damit keine zweite Datenquelle entsteht.

### Fotos: Wikimedia Commons statt Stockdatenbank

Vier echte Sülz-Aufnahmen unter freier Lizenz (CC BY 3.0 und CC BY-SA 4.0),
zugeschnitten und verkleinert. Der Bildnachweis mit Urheber, Lizenz und
Lizenzlink steht unter dem Bildstreifen — bei diesen Lizenzen ist die Nennung
Pflicht, nicht Höflichkeit. **Wer weitere Fotos ergänzt: Nachweis mitpflegen.**

### Zwei Fallen aus dieser Runde

- **Kontrast über einem Foto ist aus dem CSS nicht ablesbar.** Der helle
  Bildkopf sah gut aus, am gerenderten Screenshot gemessen fiel der Fließtext
  über dunklen Bildstellen aber auf 2,66:1. Erst ein bis unter den Text
  reichender Verlauf und Textfarbe `--ink` brachten ihn auf 5,15:1.
  Gemessen wird am Bild, nicht im Stylesheet.
- **Kartenpunkte nie schätzen.** Erneut passiert: Der Decksteiner Weiher lag
  über einen Kilometer neben dem Wasser, alle acht Punkte waren daneben. Die
  Koordinaten kommen jetzt aus Nominatim. Und die OSM-Kacheln müssen den
  ganzen Ausschnitt abdecken — die erste Fassung endete bei 50,920 und ließ
  das obere Kartendrittel leer.

Sülz ist mit 3.078 Gebäuden dichter als Deutz; Vereinfachungstoleranz 1,6 und
Mindestfläche 44 drücken die Karte auf 324 KB (rund 80 KB ausgeliefert).

**Aus Baris' Vorlage übernommen und verdichtet:** Die acht WhatsApp-Texte
enthielten denselben Stoff mehrfach — der letzte fasste alle vorherigen
zusammen. Übernommen sind Struktur und Argumente, nicht der Wortlaut; die
Seite kommt mit 1.517 Wörtern aus und hat 0 % Eigenwiederholung sowie 0 %
Bausteinanteil (kein einziger Satz, der auf einer anderen Seite steht).

**Zwei Angaben aus der Vorlage bewusst nicht übernommen:** die Zahl „rund 750
Banken" (unbelegt, § 5a UWG — steht bereits als offener Punkt in diesem
readme) und die Formulierung, Vor-Ort-Termine hätten „zu höheren
Verkaufspreisen beigetragen" (nicht belegbar). Die Verkaufsdauer nennt die
Seite mit drei bis sechs Monaten nach Baris' Angabe; **das widerspricht dem
Baustein „acht bis sechzehn Wochen" auf 61 anderen Seiten** und sollte
vereinheitlicht werden.

Cache-Buster: `styles.css?v=42` und `main.js?v=24` auf allen Seiten.

## Was in v43 umgesetzt wurde

### Lead-Cockpit: interne Live-Liste aller Kontaktereignisse

Unter `/lead-cockpit.html` liegt eine interne, nirgends verlinkte und nicht
indexierbare Seite, die jede Kontaktinteraktion der Website live zeigt
(Aktualisierung alle zehn Sekunden): Anruf angetippt, WhatsApp geöffnet,
E-Mail geöffnet, Formular abgesendet — mit Seite, Uhrzeit, Tageszählern und
optionalem Ton bei neuen Ereignissen.

**Zugang:** Der Schlüssel liegt in `lead-cockpit-zugang.txt` auf dem
Schreibtisch des Inhabers (bei der Einrichtung am 09.08.2026 dort abgelegt,
absichtlich nicht im Repository). Geprüft wird nur der SHA-256-Hash des
Schlüssels; der steht als Konstante in `lead-feed.mts` — ein Hash aus 24
Byte Zufall ist kein Geheimnis, aus ihm lässt sich der Schlüssel nicht
zurückrechnen. (Ursprünglich war eine Netlify-Umgebungsvariable geplant;
das Netlify-MCP meldete beim Anlegen zwar Erfolg, legte aber nachweislich
nichts an. Eine manuell in der Netlify-Oberfläche angelegte Variable
`LEAD_COCKPIT_TOKEN_HASH` hätte Vorrang vor der Konstante.) Schlüssel
wechseln: neuen Wert erzeugen (`openssl rand -hex 24`), Hash bilden
(`printf '%s' NEU | shasum -a 256`), Konstante ersetzen, deployen.

**Bauteile:**
- `netlify/functions/lead-track.mts` — nimmt Ereignisse per sendBeacon an.
  Whitelist der Arten, Längengrenzen, Zeitstempel serverseitig. Speichert
  KEINE IP und KEINEN User-Agent.
- `netlify/functions/lead-feed.mts` — liefert die Liste, nur mit Schlüssel
  (zeitkonstanter Hash-Vergleich). Löscht dabei häppchenweise, was älter als
  sechs Monate ist.
- `submission-created.mts` — hält zusätzlich jeden verifizierten
  Formulareingang fest (nur Formularname und Seite, keine Inhalte). Bewusst
  serverseitig: Der öffentliche track-Endpunkt akzeptiert die Art "formular"
  nicht, damit niemand Eingänge vortäuschen kann.
- `js/main.js` — meldet Klicks auf tel:-, wa.me- und mailto:-Verweise.

**Speicherformat:** Alle Angaben stecken im Blobs-Schlüssel
(`e/<Monat>/<ISO-Zeit>~…`), der Wert bleibt leer. Der Feed kommt so mit
list()-Aufrufen aus, ohne Einzel-Downloads — wichtig beim 10-Sekunden-Takt.
Felder sind URI-codiert plus `!*'()~`, weil encodeURIComponent diese Zeichen
stehen lässt und `~` das Trennzeichen ist. Und in `monatsListe` steht der
Rücksprung auf den Monatsersten VOR dem Zurückrechnen — am 31. eines Monats
liefe setUTCMonth sonst über und der Vormonat fiele aus der Abfrage.

**Rechtlicher Zuschnitt (zweistufig, datensparsam):**
- Ohne Einwilligung: nur Art, Seite, Zeitpunkt. Kein Endgeräte-Zugriff
  (§ 25 TDDDG greift nicht), keine IP-Speicherung; Art. 6 Abs. 1 lit. f.
- Mit Statistik-Einwilligung: zusätzlich eine zufällige Sitzungskennung im
  sessionStorage (endet mit dem Browser-Schließen), die Ereignisse derselben
  Sitzung verknüpft; Art. 6 Abs. 1 lit. a, § 25 Abs. 1 TDDDG.
- Datenschutzerklärung Abschnitt 11a neu; Statistik-Text im Cookie-Dialog
  auf allen 230 Seiten um die Sitzungskennung ergänzt. Wie alles Rechtliche:
  vor dem nächsten Anwaltstermin gegenprüfen lassen.

Cache-Buster `main.js?v=23` auf allen Seiten. Das Cockpit steht nicht in der
Sitemap und nicht in robots.txt (ein Disallow-Eintrag würde die Adresse
gerade veröffentlichen); es trägt noindex als Meta-Tag und als Header.

## Was in v42 umgesetzt wurde

### Köln-Deutz als erste ausgebaute Veedelseite

Beginn eines Vorhabens, das über Monate läuft: Die Stadtteil- und Themenseiten
werden einzeln überarbeitet, weg von der Vorlage hin zu eigenen Inhalten mit
Belegen und eigenen Bildern. Deutz ist die erste Seite.

**Warum überhaupt.** Die Website ist Ende Juli von 45 auf über 230 Seiten
gewachsen. Die neuen Seiten entstanden aus Vorlagen mit eingesetzten Daten. Eine
Messung über 222 Seiten hat gezeigt, woran das erkennbar ist — und woran nicht:

- Der **Schreibstil** ist unauffällig. Über 134.799 Wörter finden sich kaum
  Floskeln („zudem" 128×, „in der Regel" 19×), die Satzlängen streuen normal
  (Mittel 14,9 Wörter, Streuung 10,9). Am Stil zu feilen brächte nichts.
- Erkennbar ist die **Vorlage**: im Mittel 10,3 % des Textes einer Seite sind
  Sätze, die zweimal auf **derselben** Seite stehen; 25,5 % sind Sätze, die auf
  mehr als drei Seiten wortgleich vorkommen; die Überlappung mit der jeweils
  nächstverwandten Seite liegt im Mittel bei 51 %, bei den 55 Umlandstädten bei
  rund 75 %. Und **205 der 222 Seiten trugen kein einziges Inhaltsbild**.

Gemessen wird mit `tools/seiten-pruefen.py` (in v42 ergänzt). Ohne Argument gibt
es die Rangliste, mit Dateiname den Einzelbericht samt der konkret doppelten
Sätze, mit `--csv` eine Fassung zum Vergleich zweier Stände.

**Was Deutz jetzt hat.** Bildkopf mit echtem Ortsfoto, Kennzahlenleiste,
schematische Lagekarte als Inline-SVG, vier Tabellen (Vergleich mit der
Gesamtstadt, Objektarten und Käufergruppen, Wertfaktoren online gegen vor Ort,
Unterlagen nach Objektart), Ablauf in sieben Schritten, sechs typische Fehler und
ein Bildstreifen mit drei Motiven. Von 556 auf 2.133 Wörter, von null auf vier
Inhaltsbilder, Bausteinanteil von 4,1 auf 1,8 %. Lighthouse mobil bleibt bei
100 / 100 / 100 / 100, CLS 0,00.

### Die Karte: zwei Ansichten, echte Daten

**Orientierung** zeigt zehn Landmarken, **Bodenrichtwerte** die fünfzehn
amtlichen Zonen aus BORIS NRW — von 4.000 € je m² am Kennedy-Ufer über 3.000 €
an der Deutzer Freiheit bis zu 1.260 € an der Eitorfer Straße. Jede Fläche ist
anklickbar und nennt Wert, zulässige Nutzung, Lagebezeichnung und
Geschossflächenzahl. Diese Spreizung um den Faktor drei innerhalb eines
Stadtteils ist das stärkste Argument gegen einen pauschalen Quadratmeterpreis.

Beide Ebenen liegen im selben SVG, `js/main.js` blendet um. Erzeugt von
`tools/veedelkarten/`, dort steht auch, woher die Daten kommen und welche
Fallstricke es gab.

**Drei Anläufe, und was daraus zu lernen ist.** Google Maps läge
hinter dem Cookie-Banner und wäre für jeden unsichtbar, der ablehnt; außerdem
gingen Daten an Google. Das Inline-SVG braucht keine Einwilligung und keinen
zusätzlichen Request.

Die *erste* Fassung war nach Augenmaß gezeichnet und schlicht falsch: Die Köln
Arcaden lagen mittig statt im Osten, Hyatt und KölnTriangle untereinander statt
nebeneinander, und die Poller Wiesen standen als Deutzer Grünfläche darin,
obwohl sie in Poll liegen.

Die *zweite* projizierte echte Koordinaten, blieb aber eine leere Umrissfläche:
richtig, aber ohne Wiedererkennungswert. Der Rhein fehlte darin fast ganz — ein
Parser-Fehler, denn seine Uferlinien sind Mitglieder einer Relation und tragen
selbst keine Tags.

Erst die *dritte* Fassung mit Gebäuden, gestuftem Straßennetz und den
Bahntrassen liest sich als Stadtplan. **Lehre: bei Karten weder nach Augenmaß
setzen noch sich mit korrekten Koordinaten allein zufriedengeben.**

Die Karte wiegt 245 KB, ausgeliefert rund 56 KB — ohne
Douglas-Peucker-Vereinfachung wären es 546 KB, weil 1.600 Gebäudeumrisse jede
Hausecke einzeln mitbringen.

Jeder Punkt ist anklickbar und erklärt in einem Feld unter der Karte, was er
für den Immobilienmarkt bedeutet. Der Klick führt, nicht das Überfahren mit der
Maus — auf dem Handy gibt es kein Hover. Ohne JavaScript bleibt die Karte eine
vollständige, beschriftete Abbildung.

### Preisdiagramm: wo Deutz im Kölner Gefüge steht

Ein Balkendiagramm über alle zwanzig Stadtteile, für die der Gutachterausschuss
Kaufpreise ausweist, sortiert und mit Deutz hervorgehoben. Es macht die
Kernaussage der Seite sichtbar: Rang 10 von 20, also exakt die Mitte.

Zwei Farben, nicht zwanzig — die übrigen Werte sind bewusst zurückgenommen.
Geprüft mit dem Palettenvalidator: Trennung ΔE 34,6 bei Protanopie (Schwelle 8).
Der Neutralton bleibt mit 2,63:1 unter der 3:1-Marke gegen die Fläche; das ist
zulässig, weil jeder Balken Name und Wert als sichtbares Label trägt.

Auf schmalen Bildschirmen erscheint eine **fokussierte Fassung mit sieben
Zeilen** statt aller zwanzig: Höchstwert, die Nachbarn von Deutz, niedrigster
Wert. Der Grund steht im Skript — bei zwanzig Zeilen schneidet der Scrollbereich
ausgerechnet die Wertespalte ab, und alle Balken sähen gleich lang aus.

**Inhaltlich geradegerückt.** Die amtlichen Zahlen widersprechen dem üblichen
Maklerton. Deutz liegt beim Bodenrichtwert auf Rang 11 der 20 ausgewerteten
Stadtteile, also im Mittelfeld, nicht in der Spitze. Die Durchschnittswohnung ist
mit 64,4 m² rund ein Sechstel kleiner als im Kölner Schnitt (77,3 m²), 61,6 %
der Haushalte sind Einpersonenhaushalte (Köln: 51,9 %), nur 11,7 % haben Kinder
(Köln: 17,7 %). Deutz ist ein Stadtteil kleiner Wohnungen. Die Seite sagt das,
statt Einfamilienhäuser und Gärten in den Vordergrund zu stellen, die es dort
kaum gibt. Wer mit „Toplage" wirbt, bekommt von jedem Interessenten Widerspruch,
der den Marktbericht kennt.

**Nebenbei behoben:** Auf der alten Seite stand ein abgebrochener Satz
(„… moderne Neubauwohnungen.   Objekte in erster Rheinlage deutlich mehr.").

**Zwei Fallen, die dabei aufgetreten sind:**

- `padding: X 0` auf einem Element, das zugleich `.container` ist, setzt dessen
  seitliches Polster auf null. Auf dem Desktop fiel das nicht auf, weil der
  Container dort ohnehin zentriert steht; auf dem Handy klebte der gesamte
  Hero-Text am linken Rand. Richtig ist `padding-block`.
- Ein SVG mit 13-px-Beschriftung in einer 860er viewBox schrumpft auf einem
  390-px-Bildschirm auf rund fünf Pixel. Die Karte behält deshalb unter 560 px
  ihre Entwurfsbreite und liegt in einem seitlich beweglichen Rahmen — dieselbe
  Lösung wie bei den Tabellen, mit sichtbarem Hinweis.

**Cache-Buster:** `styles.css?v=41` und `main.js?v=22` auf allen 230 Seiten.

## Was in v41 umgesetzt wurde

### Alte Domain aufgegeben, Weiterleitungen entfernt

**Entscheidung des Inhabers vom 31.07.2026:** `highseller-immobilien.koeln`
wird nicht mehr genutzt und auch nicht auf Netlify gezeigt. Die 42
Weiterleitungen, die in v39 dafür angelegt wurden, sind deshalb aus
`netlify.toml` entfernt — sie hätten ohne Domain-Alias und DNS-Umstellung
ohnehin nie gegriffen und wären als toter Code liegen geblieben. Von 109
Regeln bleiben 67.

An ihrer Stelle steht ein Kommentarblock, der die Entscheidung festhält.
Das ist Absicht: Ohne ihn liest sich das Fehlen der Regeln später wie ein
Versehen, und jemand baut sie gutgemeint wieder ein.

**Was das kostet, damit es niemanden überrascht:** Die alte Domain antwortet
weiterhin auf jeder Adresse mit 404. Wer aus einem Google-Treffer oder über
einen alten Verweis kommt, landet im Nichts statt auf der passenden Seite.
Die dort aufgebaute Sichtbarkeit verfällt.

**Falls die Entscheidung revidiert wird**, sind zwei Schritte nötig, bevor
irgendeine Regel greifen kann. Die alten Regeln stehen in der
Versionsgeschichte von `netlify.toml`.

1. Domain in Netlify als Alias des Projekts „high-seller" eintragen, Apex und
   `www`.
2. DNS bei Strato umstellen: A-Eintrag von `81.169.145.160` auf `75.2.60.5`,
   `www` als CNAME auf `high-seller.netlify.app`.

**Achtung dabei:** An der Domain hängt E-Mail. Der MX-Eintrag zeigt auf
`smtpin.rzone.de`, Stratos Mailserver. Wer die DNS-Einträge umstellt, darf die
MX-Einträge nicht anfassen, sonst bricht der E-Mail-Empfang. Wer die Domain
kündigt, verliert jede E-Mail-Adresse darauf.

Gruppe 3 in `netlify.toml` (alte Pfade ohne Hostangabe) bleibt bestehen. Diese
Pfade gab es auf high-seller.de nie, die Regeln kosten aber nichts und fangen
händisch umgeschriebene Verweise ab.

## Was in v40 umgesetzt wurde

### Neues Teamfoto von Serhad Mendekli
Das bisherige Foto war eine Innenaufnahme vor Fensterfront und fiel damit aus der
Bildsprache der Seite heraus — Baris Ölmez steht auf seinem Portrait draußen vor
der Bebauung im Zollhafen. Das neue Foto ist an derselben Stelle entstanden und
zeigt dasselbe Gebäude im Hintergrund, die beiden Kacheln wirken jetzt als Serie.

Der Zuschnitt ist nicht mittig gesetzt, sondern an Baris' Portrait ausgerichtet:
Kopf füllt rund 39 % der Bildhöhe, Oberkante bei etwa 14 %, Gesichtsmitte bei
61 % der Breite. Ohne diese Ausrichtung stehen zwei Personen unterschiedlich groß
nebeneinander, was im Team-Raster sofort auffällt. Ausgangsdatei war eine
HEIC-Aufnahme mit 3024×4032; ausgeliefert werden wie bei allen Teamfotos
820×1040 als JPEG plus zwei WebP-Größen (400 und 820 Pixel breit).

**Wichtig — neuer Dateiname statt Ersetzen.** Die Dateien heißen
`team-serhad-2026.jpg`, `team-serhad-2026-400.webp` und
`team-serhad-2026-820.webp`. `netlify.toml` liefert `/assets/img/*` mit
`max-age=31536000, immutable` aus; Browser fragen dort ein Jahr lang nicht nach
einer neueren Fassung, auch ein harter Reload greift bei `immutable` nicht
zuverlässig. Wer den Inhalt einer Bilddatei ändert, muss ihr deshalb einen neuen
Namen geben — eine Datei unter gleichem Namen zu überschreiben wirkt live nur bei
Erstbesuchern.

Die alten `team-serhad.*` liegen vorerst weiter im Repository, weil der offene
Branch `seo/domain-duplikate-vertrauen` sie noch referenziert. Sie können
gelöscht werden, sobald dieser Branch gemergt ist. Verwiesen wird auf das neue
Foto in `index.html` und `ueber-uns.html`; geprüft wurde bei 1440 px und mit
Geräteemulation bei 390×844×3, in beiden Fällen ohne Überlauf.

## Was in v39 umgesetzt wurde

### Alte Domain: highseller-immobilien.koeln

**Das war der eigentliche Fund.** In `netlify.toml` und `_redirects` standen
Regeln für alte Adressen wie `/karriere-seite` oder `/kontaktformular`, ohne
Angabe eines Hosts. Sie sahen nach einer erledigten Domainumstellung aus, waren
aber wirkungslos: Diese Pfade gab es auf high-seller.de nie. Sie gehören zur
Vorgängerseite unter **highseller-immobilien.koeln**.

Diese Domain gibt es noch. Sie zeigt auf Strato (81.169.145.160) und antwortet
dort auf **jeder** Adresse mit einem nackten 404, auch auf `/` und
`/robots.txt`. Google führt die alten Seiten noch, jeder Klick darauf landet
im Nichts, und die aufgebauten Verweise laufen ins Leere. Belegt ist die alte
Navigation über einen Schnappschuss des Internet Archive vom 21.02.2025;
daraus stammen zwei bisher fehlende Adressen: `/impressum` und `/kalender`.

Der Nachbardomain **highseller-immobilien.de** ist eine Squarespace-Seite, die
auf „privat" steht (`noindex`, Anmeldemaske auf jeder Adresse). Sie schadet
nicht, ist aber auch kein Ziel.

In `netlify.toml` liegen jetzt **42 Regeln für die alte Domain**: je Host (Apex
und `www`) 20 unterseitengenaue Zuordnungen, die 17 alte Seiten in allen
belegten Schreibweisen abdecken, dazu je eine Auffangregel auf die Startseite.
Alle nennen den Host vollständig, und das heißt: ein einziger Sprung von der
alten Adresse auf ihr neues Ziel, statt des Umwegs über Netlifys automatische
Alias-Umleitung.

Die Auffangregel muss die **letzte** ihrer Gruppe bleiben, sonst verschluckt
sie die genauen Zuordnungen darüber. Und die ganze Gruppe muss **vor** allen
hostlosen Regeln stehen, sonst lieferte Netlify den Inhalt der neuen Seite
unter der alten Domain aus und erzeugte damit genau die Doppelung, die der
Abschnitt darunter beseitigt.

**Diese Regeln greifen erst nach zwei Schritten, die nur der Domaininhaber
ausführen kann:**

1. In Netlify unter *Project „high-seller" → Domain management → Add domain
   alias* sowohl `highseller-immobilien.koeln` als auch
   `www.highseller-immobilien.koeln` eintragen.
2. Bei Strato die DNS-Einträge umstellen. Für die nackte Domain ein
   ALIAS-/ANAME-Eintrag auf `high-seller.netlify.app`, falls Strato das nicht
   anbietet ersatzweise ein A-Eintrag auf Netlifys Lastverteiler
   `75.2.60.5`. Für `www` ein CNAME auf `high-seller.netlify.app`. Die
   Umstellung kann bis zu einen Tag brauchen.

Danach zur Kontrolle:
`curl -sI https://highseller-immobilien.koeln/karriere-seite | grep -i location`
muss `https://high-seller.de/karriere.html` liefern.

**Falle:** `_redirects` wird von Netlify **vor** `netlify.toml` ausgewertet.
Die pfadbasierten Regeln, die dort standen, hätten die neuen Host-Regeln
überholt und wegen ihres relativen Ziels von
`highseller-immobilien.koeln/karriere-seite` auf
`highseller-immobilien.koeln/karriere.html` geleitet — der Besucher wäre auf
der alten Domain hängengeblieben. Deshalb ist `_redirects` jetzt leer und
enthält nur noch diese Warnung. **Alle Weiterleitungen gehören in
`netlify.toml`.**

### Eine Seite, eine Adresse

Netlify lieferte jede Seite unter zwei Adressen mit Status 200 aus, also
`/kontakt` **und** `/kontakt.html`. Für Suchmaschinen sind das zwei Seiten mit
identischem Inhalt, die um dieselbe Suchanfrage konkurrieren. Nachgemessen
live: `/kontakt`, `/karriere`, `/immobilienmakler-koeln` und `/index.html`
lieferten alle 200.

Maßgeblich ist die `.html`-Fassung — alle canonical-Angaben, die `sitemap.xml`
und sämtliche internen Verweise zeigen darauf. Die endungslose Adresse leitet
jetzt dauerhaft dorthin, `/index.html` auf die Wurzel. 44 Seiten betroffen.
`force = true` ist dabei nötig, sonst hält Netlify die endungslose Adresse für
eine vorhandene Datei und übergeht die Regel.

`/immobilienangebote` war ein Sonderfall derselben Doppelung: eine interne
Umschreibung mit Status 200 auf `immobilien-angebote.html`, und **beide**
Adressen standen in der `sitemap.xml`. Die kurze Adresse bleibt gültig, leitet
jetzt aber weiter und ist aus der Sitemap entfernt. `/immobilien/<slug>` bleibt
eine Umschreibung mit 200: diese Seiten erzeugt die Function, sie existieren
unter keiner zweiten Adresse.

**Beim Anlegen einer neuen Seite** gehört eine Entdopplungsregel in
`netlify.toml`, sonst ist die Seite sofort wieder doppelt erreichbar.

### Verkaufte Objekte stehen jetzt im Quelltext

An der entscheidenden Stelle der Referenzseite stand nur ein leeres
`<div data-sold></div>`; die Objekte kamen erst per JavaScript aus Propstack.
Google sah eine Seite ohne Referenzen, und sobald Propstack nicht erreichbar
war oder ein Objekt dort verschwand, war der Beleg weg.

Die zehn tatsächlich als „Verkauft" geführten Objekte stehen jetzt fest im
Quelltext, die Bilder liegen selbst gehostet im Projekt, eine `ItemList` nach
schema.org beschreibt die Liste maschinenlesbar. Die Momentaufnahme liegt in
`src/data/verkaufte-objekte.json` und bleibt gültig, auch wenn Propstack
ausfällt.

Bewusst **nicht** übernommen:

- **Die Straßenadresse.** Propstack liefert sie („Rodderweg 50"), aber das sind
  verkaufte Privatimmobilien. Ort und Stadtteil genügen als Referenz.
- **Der Preis.** Propstack führt den *Angebots-*, nicht den erzielten Preis.
  Ihn als Verkaufserfolg auszuweisen wäre eine Behauptung ins Blaue (§ 5a UWG).
  Dieselbe Regel galt schon in `sold-highlights.json`.
- **Die Propstack-Titel.** Dort steht Vermarktungstext bis hin zu
  Preisnachlässen („Von 149.000,-Euro auf 125.000,-Euro"). Die Überschrift
  bildet sich stattdessen aus Objektart und Ort.

**Falle:** Propstack füllt `district` unzuverlässig — mal leer, mal
„Nordrhein-Westfalen", mal der Ort selbst. Die geprüften Stadtteile stehen
deshalb unter `kuratiert` in der JSON-Datei und überdauern jede
Aktualisierung. Ein neues Objekt meldet das Werkzeug, trägt aber nichts ein.

Aktualisieren: `python3 tools/verkaufte-objekte-aktualisieren.py`. Danach die
Änderung ansehen, besonders die Stadtteile, und committen. `js/verkaufte.js`
ist entfallen.

### Bewertungen sichtbar belegt

Der wichtigste Beleg der Seite stand nur im JavaScript: der Block mit Wertung
und Anzahl trug `display:none`, und `showFallback()` blendete ihn bei einer
Störung ganz aus — ausgerechnet dann, wenn der Besucher nach einem Beleg
sucht. Wertung (5,0) und Anzahl (53) stehen jetzt mit Stand und Quellenverweis
fest im Quelltext; `js/reviews.js` aktualisiert sie beim Abruf und blendet
nichts mehr aus.

**Bewusst ohne `aggregateRating` in den strukturierten Daten.** Google wertet
Bewertungen über das eigene Unternehmen auf der eigenen Seite als
„self-serving" und schließt solche Seiten von den Sterne-Auszeichnungen aus;
`review` und `aggregateRating` an `LocalBusiness` sind laut Google nur für
Seiten gedacht, die *andere* Betriebe bewerten. Der Beleg steht deshalb als
lesbarer Text mit Verweis auf das Google-Profil.

### Vertrauenszeile auf der Startseite

Direkt über dem ersten langen Inhaltsblock stehen jetzt vier nachprüfbare
Angaben: Google-Wertung 5,0, Anzahl 53, Erlaubnisse nach § 34c und § 34i GewO,
Standort Kranhaus 1. Jede verweist auf ihre Quelle. Die Leiste darüber
(`.trust-bar`) wirbt mit Eigenschaften, diese Zeile belegt Zahlen — deshalb
kleinere Schrift, keine großen Zahlen, kein Rahmen in der Akzentfarbe. Die
Trennlinien entstehen aus `gap:1px` auf farbigem Grund und passen sich damit
jedem Umbruch von selbst an.

### Netlifys Pretty URLs abgeschaltet

Das war die zweite Hälfte des Doppelungsproblems und fiel erst beim Nachmessen
der Live-Seite auf. „Pretty URLs" ist bei Netlify **standardmäßig an** und
schreibt beim Deploy jeden internen Verweis um: Im Quelltext steht
`href="kontakt.html"`, live kam `href='/kontakt'` an. Alle internen Verweise
zeigten damit auf die endungslose Adresse, während canonical und `sitemap.xml`
auf die `.html`-Fassung zeigen — und beide antworteten mit 200.

Mit den Entdopplungsregeln allein wäre daraus ein neues Problem geworden: Jeder
Menüklick hätte erst eine 301 abgeholt. Deshalb `pretty_urls = false`.

**Merkhilfe:** Wer die Weiterleitungen prüft, muss den **ausgelieferten**
Quelltext ansehen (`curl`), nicht die Datei im Projekt. Netlify verändert das
HTML zwischen beidem.

### Die letzten drei Stadtteil-Paare entdoppelt

Der Wohnkennzahlen-Absatz wechselt harte Zahlen mit deutenden Sätzen ab. Die
Zahlen sind je Stadtteil verschieden, die Deutungssätze stammen aus einem
kleinen Vorrat — haben zwei Veedel ähnliche Werte, greifen sie zur selben
Fassung. Daraus entstanden die drei verbliebenen Seitenpaare über 20 %.

Je Gruppe bleibt ein Vorkommen unverändert, nämlich das, auf das die
Formulierung am genauesten passt; die übrigen zwölf Stellen haben eine eigene,
an den echten Zahlen geprüfte Fassung bekommen.

**Drei der alten Sätze waren dabei sachlich schief** — die Entdopplung hat
also nicht nur Text verändert, sondern Fehler behoben:

- Niehl: Förderquote 7,8 % gegen 6,2 % ist nicht „nahe am städtischen Wert",
  sondern darüber.
- Bayenthal: 3,4 % gegen 6,2 % ist deutlich darunter, ebenfalls nicht „nahe".
- Porz: 46 % Einpersonenhaushalte gegen 52 % ist gerade **keine** ausgeglichene
  Mischung, sondern ein Familienüberhang. Der alte Satz behauptete das
  Gegenteil der Daten.

| | vorher | jetzt |
|---|---|---|
| Duplikation im Mittel | 9,9 % | **9,4 %** |
| höchster Wert | 21,5 % | **20,0 %** |
| Seitenpaare über 20 % | 3 | **0** |

Skript: `tools/stadtteile-deutungssaetze-entdoppeln.py` — es hält fest, welche
Fassung zu welchem Stadtteil gehört und warum.

### Gemessener Stand der Sichtbarkeit (29.07.2026)

Alle 46 Sitemap-Adressen live abgerufen: 46 von 46 mit Status 200, keine
Umleitung, alle `index,follow`, alle mit genau einer H1, canonical und
strukturierten Daten, keine fehlende Beschreibung (125–165 Zeichen), 683 bis
2886 Wörter je Seite. Lighthouse mobil gegen die Live-Startseite: SEO 100,
Best Practices 100, Barrierefreiheit 97 → nach der Unterstreichung der
Fließtext-Verweise 100.

Doppelte Titel und Beschreibungen gab es genau einmal: `/immobilienangebote`
gegen `/immobilien-angebote.html`. Behoben.

### Weiterhin offen und nur vom Kunden lösbar

- **Die beiden Schritte zur Domain oben.** Ohne sie bleibt
  highseller-immobilien.koeln bei Strato, und keine der 42 Regeln greift.
  Einen Domain-Alias kann man **nur** über die Netlify-Oberfläche eintragen;
  weder das MCP noch die hier verfügbaren Werkzeuge können das.
- **„500+ begleitete Vorgänge"** (Hero, Trust-Leiste, Referenzseite) und
  **„Zugang zu 750+ Banken"** (46 Seiten) sind unverändert unbelegt (§ 5a UWG).
  Beide Zahlen lassen sich von außen nicht prüfen und wurden deshalb weder
  belegt noch geschönt. Belegbar sind bislang nur die 53 Google-Bewertungen
  und die zehn in Propstack als verkauft geführten Objekte.
- **Search Console ist angebunden**, anders als hier bis v38 vermerkt:
  `GSC_SA_KEY` und `GSC_STATUS_TOKEN` liegen seit dem 15.07.2026 in den
  Netlify-Umgebungsvariablen, die Function `gsc-status` fragt
  `sc-domain:high-seller.de` ab. Beide Variablen sind als geheim markiert und
  lassen sich nicht mehr auslesen — wer den Status abrufen will, braucht den
  Token aus einer eigenen Aufzeichnung:
  `curl "https://high-seller.de/.netlify/functions/gsc-status?key=<TOKEN>"`.
  Nach der Domainumstellung dort zusätzlich die alte Domain als Property
  anlegen und die Adressänderung melden, sonst dauert die Übernahme unnötig
  lange.

## Was in v37–v38 umgesetzt wurde

### Kontaktleiste auf dem Handy (Audit 1.3)
Die Leiste am unteren Rand gab es bereits, sie bot aber nur Anruf und WhatsApp —
ausgerechnet die kostenlose Bewertung, der Geschäftszweck der Seite, fehlte.
Jetzt drei Ziele, die Bewertung zuerst und farblich abgesetzt. Auf der
Bewertungsseite springt sie in den Rechner statt auf die eigene Seite.
Dazu drei Punkte, die vorher fehlten: `env(safe-area-inset-bottom)` (die Leiste
lag auf iPhones mit Home-Indicator teils unter dessen Balken), Einblenden erst
ab 600 px Scrolltiefe (im Hero stehen dieselben Aufrufe bereits groß; ohne
JavaScript bleibt sie dauerhaft sichtbar) und ein GA-Ereignis je Klick, das nur
nach Einwilligung tatsächlich sendet. Geprüft bei 320/360/390/430 px.

### Politur (Audit 3.1, 3.3, 3.8)
- **Einblendungen von 401 auf 228 Elemente**: eine Bewegung je Abschnitt statt
  einer je Karte. Die gestaffelten Verzögerungen (`data-d`) sind damit
  gegenstandslos und entfallen.
- **Vertrauen am Absendeknopf**: kostenlos, Antwort in der Regel binnen 24
  Stunden, keine Weitergabe an Dritte — direkt dort, wo Eigentümer zögern.
- **Fehlerfall nennt die Telefonnummer**. Wer beim mailto-Rückfall strandet, hat
  oft kein eingerichtetes Mailprogramm; ohne Nummer ist der Kontakt weg.

### Entdopplung der Stadtteilseiten mit amtlichen Wohnkennzahlen (Audit 2.1)
Zweite amtliche Quelle nach den Bodenrichtwerten: **Statistischer Datenkatalog
der Stadt Köln** (Amt für Stadtentwicklung und Statistik, Stand 2025) mit
Wohnungsbestand, mittlerer Wohnfläche, Haushaltsstruktur, Fertigstellungen,
Förderquote und Durchschnittsalter. Daten in
`src/data/stadtteile-wohnkennzahlen.json` samt Pflegehinweis.

Jede Seite bekommt daraus einen eigenen Absatz mit Vergleich zum Kölner Mittel
und einer Folgerung für Verkäufer. **Die Daten bestimmen, welcher von vier
Blickwinkeln erscheint**, je Blickwinkel stehen drei Fassungen bereit — sonst
wäre daraus derselbe Fehler geworden wie beim ersten Marktdaten-Anlauf, wo
gleicher Text auf 20 Seiten die Duplikation von 41,6 auf 45,5 % trieb.

Gemessen über 5-Wort-Folgen im redaktionellen Inhalt, ohne Menü, Fußzeile,
Cookie-Banner und Wertrechner-Kacheln:

| | vorher | jetzt |
|---|---|---|
| Duplikation im Schnitt | 15,6 % | **8,9 %** |
| Seitenpaare über 20 % | 99 von 190 | **0** |
| Wörter je Seite | 485 | **582** |

Nach der bisherigen Messweise, die den Cookie-Banner mitzählt: 37,4 → 29,3 %.
Dieser Rest ist Boilerplate und auf allen Seiten technisch identisch.

**Zwei Fallen dabei:**
- Sechs Stadtteilnamen (Porz, Mülheim, Nippes, Ehrenfeld, Lindenthal,
  Rodenkirchen) sind zugleich Stadtbezirksnamen. Wer nur nach dem Namen sucht,
  schreibt Bezirkszahlen auf die Stadtteilseite — Rodenkirchen hätte 58.536
  statt 9.557 Wohnungen gehabt. Immer `RAUMEBENE=Stadtteile` filtern.
- Neubau darf nicht absolut bewertet werden: 568 Fertigstellungen sind in
  Marienburg 12,9 % des Bestands, in der Innenstadt wären sie ein Rundungsfehler.
  Der Text misst die Quote am eigenen Bestand und nennt bei Sprüngen das Vorjahr.

**Weiterhin offen und nur vom Kunden lösbar:** die unbelegten „500+ begleitete
Vorgänge" und „Zugang zu 750 Banken" im Hero (§ 5a UWG), sowie Search Console
einrichten und Sitemap einreichen.

## Was in v25–v29 umgesetzt wurde (Audit-Umsetzung)

### Rechtlich (Stufe 0)
- **Google Analytics lud ohne Einwilligung** — der schwerwiegendste Punkt. In allen
  45 Dateien stand `gtag.js` fest im `<head>` und lief unabhängig vom Cookie-Banner,
  während die Datenschutzerklärung das Gegenteil behauptete (§ 25 TDDDG).
  Bemerkenswert: Die Consent-Logik in `js/main.js` war bereits korrekt gebaut —
  `loadAnalytics()` lief nur nach Zustimmung. Der `<head>`-Block lief einfach daneben her.
  Jetzt: **Google Consent Mode v2** mit `default: denied` vor allem anderen, Tag wird
  erst nach Zustimmung nachgeladen, bei Widerruf `update: denied` plus Löschen von
  `_ga`, `_ga_*`, `_gid`. Consent-Key **`hs_consent_v2` → `hs_consent_v3`**, weil die
  alte Zustimmung unter falscher Beschreibung eingeholt wurde — alle Besucher werden
  einmal neu gefragt. Datenschutzerklärung beschreibt jetzt exakt dieses Verhalten.
- **Seite ohne JavaScript unsichtbar**: `.reveal{opacity:0}` wurde nur per JS
  aufgehoben. Jetzt ist sichtbar der Grundzustand, die Animation hängt an einer
  `js`-Klasse. Zusätzlich in `main.js`: kein IntersectionObserver → sofort zeigen,
  „Bewegung reduzieren" → sofort zeigen, und ein 3-Sekunden-Netz.
- **Maps-Hinweis unlesbar**: `.section--navy .map-consent p` färbte den Text hell,
  der Kartenplatzhalter hat aber immer einen hellen Kasten. 1,75:1 → **7,14:1**.
- `prefers-reduced-motion`: Der globale Block existierte bereits (anders als im
  Audit angenommen) und wurde um `animation-iteration-count` und Pseudoelemente ergänzt.

### Performance (Stufe 1)
- **Bilder auf WebP mit `srcset`**: 26 Bilder in vier Breiten (480/960/1280/1600 bzw.
  1920), 98 Dateien, JPEG bleibt Rückfall. Erzeugt mit PIL, nicht im Browser.
  Gemessen über 19 Seiten: **8183 KB → 2980 KB auf dem Handy (−64 %)**, −61 % am Desktop.
  Die 1280er Stufe ist bewusst dabei: Ein 390-px-Handy mit 3-fachem Display braucht
  rund 1170 Bildpunkte und hätte sonst zur 1600er gegriffen.
- **Logos als WebP**: Die SVGs waren keine echten Vektoren, sondern Auto-Trace-Pfade
  aus einem PNG. Brotli ist aktiv, also gingen nicht 460 KB über die Leitung, sondern
  70 + 85 KB — jetzt **19 + 31 KB**. Im Zoom ist das WebP sogar sauberer als das SVG,
  weil die Trace-Artefakte wegfallen. SVG bleibt als Rückfall im `<picture>`.
- **Hero-Preload** lädt nicht mehr das 250-KB-JPEG, sondern per `imagesrcset` die
  passende WebP-Größe.
- **Hero auf breiten Schirmen**: Rechts steht ab 1180 px ein Einstieg in den
  Wertrechner (Objektart wählen → springt in den Rechner und wählt dort vor). Das
  stärkste Element der Seite lag vorher anderthalb Bildschirmhöhen tiefer.
- Ein Sticky-CTA war **bereits vorhanden** (`.mobile-bar`), anders als im Audit vermerkt.

### Drei Layout-Fehler, die dabei auffielen
Alle drei haben dieselbe Wurzel — **`min-width:auto` auf Grid- und Flex-Kindern**:
- Qualifikations-Karten sprengten zwischen 640 und 860 px die Seite (825 statt 760 px),
  weil „Immobiliardarlehensvermittler" seine Spalte auf 325 px aufblies.
- Der Budgetrechner lief bei 600 px auf 767 px, weil eine Schaltfläche in einer 187 px
  schmalen Karte ihre Eigenbreite hielt.
- Die `min-width:0`-Regeln standen bisher **nur** im 560-px-Block und wurden auf alle
  Breiten gehoben.
- Dazu ein Fehler, den erst der Umstieg auf `<picture>` erzeugt hat: `.media-frame`
  hat `aspect-ratio` und streckte sich auf die Zeilenhöhe der Nachbarspalte — daraus
  rechnete es 866 statt 431 px Breite zurück. Behoben mit `width:100%` am Rahmen,
  plus `picture{display:contents}`, damit das Element gar nicht erst als eigene Box
  ins Layout eingreift.
Geprüft über 108 Kombinationen aus 12 Seiten und 9 Breiten (320–1920 px): kein Überlauf.

### Barrierefreiheit & Auszeichnung (Stufe 2)
- **Sichtbarer Tastaturfokus** (2.3): Es gab drei `outline:none`-Stellen, davon eine
  ganz ohne Ersatz (Newsletter im Footer). Jetzt durchgehende `:focus-visible`-Regeln
  mit heller Variante auf den dunklen Flächen. Auf der Startseite geprüft: alle
  **112** fokussierbaren Elemente haben einen sichtbaren Rahmen. Der sechsstufige
  Wertrechner wurde per Tastatur durchlaufen — Kacheln wählbar, Pflichtfeldprüfung
  meldet verständlich („Bitte geben Sie eine gültige Postleitzahl an").
- **Schema.org** (2.7): `geo` mit echten Koordinaten (über OpenStreetMap für
  „Im Zollhafen 18" ermittelt, nicht geschätzt) und `sameAs` mit sechs geprüften
  Profilen in alle neun `RealEstateAgent`-Blöcke. `BreadcrumbList` auf 11 weiteren
  Seiten ergänzt — abgeleitet aus dem **sichtbaren** Brotkrumenpfad, damit Anzeige
  und Auszeichnung nicht auseinanderlaufen. Kein `aggregateRating`.
  `openingHoursSpecification` und `FAQPage` waren entgegen dem Audit bereits vorhanden.
- **Brotkrumen vereinheitlicht**: Ehrenfeld nutzte „Start › Standorte ›", die anderen
  19 Stadtteilseiten „Start › Köln ›". Ehrenfeld angeglichen — eine Datei statt 19.
- Validierung über alle Seiten: 43 BreadcrumbList, 20 FAQPage, 9 RealEstateAgent,
  2 JobPosting, **0 Fehler**.

### Gemessen (Lighthouse, mobil)
| | live (alter Stand) | lokal (neu) |
|---|---|---|
| Accessibility | 100 | 100 |
| Best Practices | 92 | 96 |
| SEO | 100 | 100 |
| Fehler | 2 | 1 (lokales Artefakt) |

Beide Fehler der Live-Seite waren **Google Analytics**: Der Tag feuerte ohne
Einwilligung und wurde dabei von der eigenen CSP blockiert. Der verbleibende
Fehler lokal ist ein 404 auf die Netlify-Function, die der Testserver nicht kennt.

Performance lokal unter Slow 4G und 4-facher CPU-Drosselung:
**LCP 770 ms** (Ziel < 2500), **CLS 0.00** (Ziel < 0,1). Achtung: TTFB war dabei
0,6 ms, weil localhost. Live kommt die Serverlatenz dazu — realistisch eher
900–1100 ms, weiterhin klar im grünen Bereich.

**CSP-Fehler gefunden und behoben**: `connect-src` erlaubte
`region1.google-analytics.com`, GA4 sendet aber an `region1.analytics.google.com`
— andere Reihenfolge der Namensteile, deshalb blockiert. Das wäre nach der
Consent-Umstellung bei jedem zustimmenden Besucher aufgetreten. Jetzt über
Platzhalter (`*.analytics.google.com`) abgedeckt.

### Sichtbarkeit (Stufe 2.1 / 3.6)
Gemessen statt geschätzt — und die Lage ist schlechter als im Audit vermerkt:

**Textduplikation zwischen den 20 Stadtteilseiten** (5-Wort-Folgen, Hauptinhalt
ohne Menü und Fußzeile): Durchschnitt **43,3 %**, Spitzen über 52 %,
**alle 190 Seitenpaare** liegen über 20 %. Das Audit nannte 31 % für ein Paar.
Seitenlänge 481–708 Wörter. Das ist Doorway-Page-Gebiet — Google kann das als
geringwertig einstufen und die ganze Domain mit abwerten.

**Technisch war dagegen wenig zu holen** — das war bereits sauber:
keine doppelten Titel oder Beschreibungen, alle 44 Beschreibungen in guter Länge,
überall genau eine H1, canonical und `lang` vollständig, robots.txt korrekt mit
Sitemap-Verweis.

Was umgesetzt wurde:
- **`lastmod` in der Sitemap** — fehlte bei allen 45 Einträgen komplett.
- **Interne Verlinkung der Stadtteile nach amtlichem Stadtbezirk**: von 34 auf
  **99 Querverweise** (1,7 → 5,0 je Seite). Die Zuordnung ist symmetrisch
  aufgebaut, sonst hängen Randlagen wie Porz und Pesch in der Luft — beide hatten
  vorher **null** eingehende Querverweise. Jetzt hat jede Seite mindestens zwei.
- **`RealEstateAgent` auf 15 weiteren Stadtteilseiten**: Nur 5 von 20 hatten eine
  Firmenauszeichnung mit `areaServed`. Für lokale Suchanfragen ein echter Nachteil.
  Jetzt 24 Blöcke site-weit, alle mit `geo` und `sameAs`.
- **Eigene 404-Seite** (`404.html`): Es gab keine. Wer auf einem toten Link landete,
  sah die englische Netlify-Standardseite — ohne Logo, Navigation oder Telefonnummer.
  Jetzt im Seitendesign mit Anruf-Schaltfläche und vier häufig gesuchten Zielen,
  `noindex,follow` und ohne canonical.

Offen und **nur mit echten Daten lösbar**: die inhaltliche Entdopplung der
Stadtteilseiten. Dafür braucht es Bodenrichtwerte aus BORIS NRW beziehungsweise
dem Grundstücksmarktbericht Köln sowie stadtteilspezifische Angaben zu Bebauung
und Lage. Geschätzte Zahlen wären hier derselbe Fehler wie die unbelegten „500+".

### Suchbegriffe der Stadtteilseiten (v32)
Die Titel zielten ausschliesslich auf "Immobilienmakler Koeln-X". Von fuenf
Kernbegriffen (bewerten, Wert, Verkauf, Preis, Makler) deckte der Titel genau
einen ab — wer "Immobilienwert Lindenthal" suchte, fand nichts, obwohl die
Leistung auf der Seite steht.

- Titel um den Bewertungsteil erweitert, drei Fassungen rotierend. Das
  etablierte Hauptwort bleibt vorn, sonst braechen vorhandene Platzierungen
  fuer "Immobilienmakler Koeln-X" weg. Alle 49-60 Zeichen, keine Dopplung,
  og:title und twitter:title mitgezogen.
- Die Ueberschrift im Wertrechner-Block traegt auf allen 20 Seiten Stadtteil
  plus Wert- oder Bewertungsbegriff.
- **Falle dabei:** Auf Bayenthal, Klettenberg und Niehl erzeugte die Rotation
  exakt dieselbe H2 wie der bereits vorhandene Abschluss-Aufruf am Seitenende.
  Die Auswahl weicht jetzt aus, wenn eine Fassung anderswo auf der Seite steht.
- **Testfalle:** Der iframe-Cache lieferte beim Nachpruefen hartnaeckig die
  alten Titel, obwohl Dateien und Server bereits korrekt waren. Nach Aenderungen
  an Titeln oder Metadaten direkt an den Dateien oder per curl pruefen, nicht
  ueber einen wiederverwendeten iframe.

Die uebrigen Unterseiten blieben unveraendert: eigene Suchintention, Ortsbezug
vorhanden, Laenge passend. Dort "Immobilienwert" hineinzuzwingen wuerde schaden.

### Kleinere Punkte
- `preconnect`/`dns-prefetch` auf `images.propstack.de` — nur auf den drei Seiten,
  die Objektbilder laden.
- `twitter:title`, `twitter:description`, `twitter:image` auf allen 44 Seiten ergänzt.
- Datenschutz: **Netlify** und **Propstack** namentlich benannt, inklusive
  Drittlandübermittlung und Auftragsverarbeitung.

## Was in v24 umgesetzt wurde
- **Klebender Kopf repariert (site-weit)**: `body{overflow-x:hidden}` machte den
  Body zu einem eigenen Scrollbereich — darin greift `position:sticky` nicht mehr.
  Der Header scrollte deshalb auf **jeder** Seite und in **jeder** Breite weg,
  obwohl er als sticky angelegt war. Jetzt `overflow-x:clip` (schneidet genauso ab,
  ohne Scrollbereich); `hidden` bleibt als Rückfall für ältere Browser davor stehen.
- **Unsichtbare Schaltflächen behoben**: `.btn--ghost` ist für helle Flächen gebaut
  (fast schwarze Schrift, kein Hintergrund) und stand auf dunklem Navy — Kontrast
  1,05:1. Betroffen: Anruf-Button im Handy-Menü (44 Seiten), die beiden
  Karten-Schaltflächen im Kontaktbereich der Startseite, Telefon-Button auf der
  Ehrenfeld-Seite. Behoben über Kontextregeln (`.mobile-menu`, `.section--navy`,
  `.usp-card`, `.hero`, `.page-hero`, `.footer`), nicht Fundstelle für Fundstelle.
  Ebenso: Widerrufs-Hinweis in der dunklen `.usp-card` des Budgetrechners,
  `.eyebrow--gold` im `.valuation-band`, `.value-points` auf dunklem Grund,
  `.footer__disc` und `.footer-newsletter__eyebrow` (lagen bei 3,87 bzw. 4,18).
  Nachgemessen im Browser bei 390 px: alle 44 Seiten ohne Text unter 4,5:1.
- **Sprungleiste auf der Startseite** (`.jumpbar`, nur unter 1120 px): klebt unter
  dem Kopf, markiert den Abschnitt, in dem man gerade steht, und springt auf Tipp
  dorthin. Grund: 24 Bildschirmhöhen Länge ohne jeden Wegweiser.
- **Qualifikations-Karten auf dem Handy zweispaltig**: eine ältere Regel stellte
  diesen Block bis 640 px auf eine Spalte — 1514 px für sechs kurze Karten.
  Jetzt 714 px.
- **Karriere**: zwei ausgeschriebene Stellen (Akquisiteur, Immobilienmakler) mit
  Aufgaben, Anforderungen und Direktbewerbung; Klick auf „Auf diese Stelle
  bewerben" wählt die Stelle im Formular vor. JobPosting-Auszeichnung für Google
  Jobs, Titel und Beschreibung angepasst.
- **Impressum**: Abschnitt „Verbraucherstreitbeilegung / Universalschlichtungs-
  stelle" entfernt. **Datenschutz**: Stand auf den 28. Juli 2026 gesetzt.
- **LinkedIn-Symbol entfernt** (44 Seiten): verwies auf `linkedin.com` statt auf ein
  Profil. Alle übrigen Profil-Links live geprüft und in Ordnung; der YouTube-Kanal
  ist bestätigt, sein „noch eintragen"-Vermerk im Markup ist weg.
- **Weiterleitungen geprüft**: alle 23 Regeln aus `_redirects` und `netlify.toml`
  live gegen high-seller.de getestet, alle 44 Seiten liefern Status 200. Es war
  keine Weiterleitung defekt — der Eindruck kam von den unsichtbaren Schaltflächen
  und dem nicht klebenden Kopf.

## Was in v11 umgesetzt wurde
- **Header-Responsive**: Zusammenquetschen im Bereich 1120–1320 px behoben
  (kompaktere Nav-Stufe, `flex-wrap:nowrap`, kleineres Logo); Burger-Menü darunter.
- **Propstack-Anbindung (serverseitig)**: Netlify Functions `propstack-properties`
  (Liste) und `property` (SEO-Detailseite `/immobilien/<slug>`), gemeinsame Logik in
  `_lib/propstack.mts`. API-Schlüssel nur über `PROPSTACK_API_KEY` (Env), nie im Frontend.
  Neuer Bereich „Aktuelle Immobilienangebote“ (Startseite), Übersicht `/immobilienangebote`
  mit Filtern, Edge-Caching, Lazy Loading, freundlicher Fallback-Meldung, Schema.org.
- **Formulare auf Netlify Forms**: alle Formulare an info@high-seller.de (sendmail.php
  entfernt), Spam-Honeypot, gestaltete HTML-Benachrichtigung via
  `netlify/functions/submission-created.mts` (optional über Resend). Registrierung
  JS-/laufzeitgerenderter Formulare in `__forms.html`.
- **Google-Bewertungen**: automatische Anonymisierung („Mi*** R.“), sanftes Einblenden,
  Hover-Effekt, Google-Badge (`js/reviews.js`).
- **Auszeichnungen**: „+500 Verkäufe“ entfernt, verbleibende Siegel größer/edler.
- **Google-Karte**: adressbasierter Embed (zeigt zuverlässig Kranhaus 1, Im Zollhafen 18).
- **Footer**: Instagram/TikTok verlinkt, LinkedIn ergänzt; Facebook/LinkedIn/ImmoScout24/
  Immowelt/Kleinanzeigen als dokumentierte Platzhalter (`data-profile-todo`).
- Cache-Busting v11; Details siehe `.netlify/results.md`.


# Highseller Immobilien & Finanzen — Website (Stand v10)

## Was in v10 umgesetzt wurde
- **Header ohne CTA-Button**: „Beratung anfragen" aus dem Header entfernt. Neu ausbalanciert:
  Logo links, Navigation gruppiert, Telefonnummer rechts als dezente Pill (dort, wo zuvor der Button
  war). Kein Overflow mehr auf Desktop/Tablet/Mobil (per Messung geprüft; Telefon zeigt ab 1120 px,
  darunter Burger-Menü).
- **Newsletter neu gestaltet**: kompakte, elegante Karte im Footer statt des breiten Bandes.
  Gold-Eyebrow „Newsletter", Überschrift + Kurztext links, E-Mail-Feld und „Anmelden" als eine
  weiße Pill rechts, DSGVO-Hinweis darunter. Auf Mobil sauber gestapelt.
- Cache-Busting v10; alle 38 Seiten validiert.


## Was in v9 umgesetzt wurde
- **Header-Fix**: rechts wird nichts mehr abgeschnitten (kompaktere Navigation, kürzeres CTA
  „Beratung anfragen", Telefonnummer erst ab 1500 px, kein Overflow, per Messung verifiziert).
- **Hero**: zusätzlicher, sehr dezenter Lichtstreif (heroSheen, alle 13 s) + weicherer Glow;
  beides nur transform/opacity, respektiert prefers-reduced-motion.
- **Störende Striche entfernt**: Eyebrow-Akzentlinien (u. a. „Für Eigentümer") seitenweit deaktiviert.
- **Wertrechner**: 7 neue, konsistente Icons je Immobilienart; bei Grundstücken wird der Schritt
  „Zustand & Ausstattung" automatisch übersprungen (vor und zurück).
- **Team**: „28 Jahre Verkaufserfahrung", seriösere persönliche Vorstellungen, Zitat-Stil mit
  goldener Linie im Overlay.
- **Bilder-Ordner (8 Motive)** eingebaut: Bild-Heros für 11 Unterseiten (Verkaufen, Bewerten,
  Angebote, Käuferkartei, Baufinanzierung, Über uns, Kontakt, Wissen, Checkliste, Makler Köln, FAQ)
  über neue page-hero--img Variante; alle SEO-benannt mit Alt-Texten.
- **Hintergründe**: feine Linienstruktur in hellen Sektionen, radiale Lichtflächen in dunklen,
  edlere Verläufe in page-hero und Footer.
- **Widerruf**: E-Mail-Button öffnet das Mailprogramm mit vollständiger Widerrufsvorlage im Text
  (Empfänger, Betreff, Vorlage; Nutzer ergänzt nur noch seine Daten).
- **Newsletter**: große Startseiten-Sektion entfernt; stattdessen dezente, kompakte Box im Footer
  aller Seiten (E-Mail + Einwilligung + Double-Opt-in-Hinweis über sendmail.php).
- **Neue Seite verkaufte-objekte.html**: Referenzseite mit Bild-Hero, 6 Referenzkarten
  (Verkauft-Badge, Ort, Objektart, Flächen; diskret ohne Preise), Vertrauens-Split und Bewertungs-CTA;
  in Navigation, Footer und Sitemap verlinkt. ACHTUNG: Karten sind Beispieldaten, vor Livegang durch
  echte, freigegebene Referenzen ersetzen (Kommentar im Code).
- **Cache-Busting v9**; alle 38 Seiten validiert (Tag-Struktur, Links, Assets).


## Was in v8 umgesetzt wurde
- **Gedankenstriche entfernt**: alle „ – " in Fließtexten seitenweit grammatikalisch aufgelöst
  (Komma/Punkt); sichtbare Komposita wie „Budgetrechner" vereinheitlicht. Zahlenspannen und
  E-Mail/Vor-Ort-Schreibweisen bleiben korrekt.
- **Navigation**: Menüpunkt „Startseite" (Desktop + Mobil), Header mit mehr Luft (92 px).
- **Ansprechpartner**: „Callcenter"-Punkt ersetzt durch „Zugang zu über 750 Banken über unser
  Finanzierungsnetzwerk"; überall „29 Jahre Verkaufserfahrung".
- **Team**: Name/Rolle als Overlay im Bild, persönlichere Vorstellungen (Baris mit dezentem Schmunzler).
- **Sterne in Gold** (#E4B33C) auf der gesamten Seite; Google-Bewertungen laufen künftig als ruhige
  Marquee-Kartenreihe (js/reviews.js rendert automatisch, sobald echte Rezensionen eingetragen sind).
- **Footer**: Claim unter dem Logo hervorgehoben (footer__claim), Social-Icons in Markenfarben (Hover),
  Portal-Einträge mit Farb-Icons + echtem Google-G, Widerruf-Button harmonisch in der Legal-Zeile.
- **Impressum**: Berufsbezeichnungen korrigiert (Immobilienmakler nach § 34c GewO,
  Immobiliardarlehensvermittler nach § 34i GewO, Hausverwalter nach § 34c GewO), auch im Footer-Disclaimer.
- **Budgetrechner**: „Einnahmen & Ausgaben" (ohne „Aus"), Haushaltsnettoeinkommen vor Personen,
  13 Info-Tooltips; Finanzierungsrechner 8 Tooltips; Wertrechner 3 Tooltips (Komponente .info-tip,
  Hover + Fokus/Klick, mobil nutzbar).
- **Kontakt**: „Gewünschte Leistung" mit Optgroups (Immobilien/Finanzierung) und neuen Optionen
  (verkaufen, bewerten lassen, kaufen, Finanzierungsberatung, Baufinanzierung prüfen,
  Anschlussfinanzierung, Allgemeine Anfrage).
- **Neue Fotos** (SEO-benannt): koeln-panorama-dom-nacht, schluesseluebergabe-immobilienverkauf-koeln
  (Prozess), handschlag-immobilienmakler-koeln (Kontakt), immobilienmakler-schreibtisch-koeln
  (Verkaufen), expose-beratung-immobilienmakler (Käuferkartei).
- **Awards**: Siegel-Grafiken einheitlich (84 px, contain) in den Referenz-Kacheln.
- **Design**: dezente Verläufe (soft/navy/page-hero/footer), Overscroll-Flächen behoben
  (html-Hintergrund navy), Cache-Busting v8.


## Was in v7 umgesetzt wurde
- **500+ Immobilienverkäufe** seitenweit (Hero, Trust-Leiste, Referenzen, Über uns, Kontakt).
- **Kontakt**: Headline „Ich freue mich darauf, Sie persönlich kennenzulernen."; Beratungsbild auf der
  Startseite; Trust-Zeile (24-h-Antwort, kostenlos, 500+ Verkäufe); Formular in Segmente
  „Immobilienverkauf/Bewertung" und „Finanzierung" getrennt (main.js).
- **WhatsApp-Schwebebutton entfernt** (mobile Kontaktleiste und Menü-Links bleiben).
- **Ladebildschirm**: dezenter Loader mit Logo auf der Startseite, nur einmal pro Sitzung (sessionStorage).
- **Wertrechner**: PLZ, Ort, Stadtteil, Straße, Wohnfläche, Grundstück (falls relevant) und Baujahr sind
  Pflichtfelder; Unverbindlichkeits-Hinweis („ohne Gewähr") auf Startseite und Bewertungsseite.
- **Bewertungs-CTA**: „Ihre Meinung macht den Unterschied."
- **Neue Seite unterlagen-checkliste.html**: alle Verkaufsunterlagen nach Kategorien, Energieausweis-Fakten
  (10 Jahre gültig, Pflicht), druckfreundliche Checkliste mit Logo-Wasserzeichen (window.print), in
  Navigation und Sitemap verlinkt.
- **15 neue Stadtteilseiten** (Deutz, Klettenberg, Bayenthal, Marienburg, Mülheim, Porz, Weidenpesch,
  Niehl, Junkersdorf, Braunsfeld, Innenstadt, Zollstock, Dünnwald, Höhenhaus, Pesch) mit einzigartigen
  Texten, FAQ inkl. FAQPage-Schema, CTAs und Querverlinkung; Übersichtsseite verlinkt alle 20 Veedel.
- **FAQ**: 4 neue Fragen (Bewertungsablauf, Vor-Ort vs. Online, Marktwert Köln), Schema auf 32 Fragen erweitert.
- **Google Maps**: Embed auf „Highseller Immobilien & Finanzen, Im Zollhafen 18, 50678 Köln" (Klick-Consent bleibt).
- **Widerruf**: Footer-Link als sichtbarer Button „Vertrag widerrufen".
- **Performance**: Hero-Preload, decoding=async für alle Bilder, Cache-Busting (?v=7) für CSS/JS.


## Was in v6 umgesetzt wurde (Helles Blau · Wertrechner · Stadtteile)
- **Farbkonzept**: Gold vollständig durch helles, seriöses Blau ersetzt (#2F7CD3 / #2263AE); Buttons,
  Sterne, Akzente, Rechner-Highlight und Formular-Fokus angepasst; Gesamtwirkung heller.
- **Hero**: dezenter Ken-Burns-Zoom auf dem Hintergrundbild + weicher Licht-Glow (beides respektiert
  prefers-reduced-motion), aufgehelltes Overlay, Text-Schatten für optimale Lesbarkeit.
- **Ausführlicher Wertrechner (6 Schritte)** jetzt direkt auf der Startseite, inklusive
  PLZ-zu-Stadtteil-Automatik in js/wertrechner.js; kompaktes Bewertungsformular ersetzt.
- **Neue Bilder** (SEO-benannt): kranhaeuser-koeln-rheinauhafen.jpg (Standorte/Über uns/Makler Köln),
  immobilienberatung-koeln.jpg (Kontakt/Über uns), marktanalyse-immobilienbewertung-koeln.jpg
  (Baufinanzierung/Wissen). Zwei gelieferte Motive wegen KI-Artefakten bewusst nicht verwendet.
- **Wissen & Ratgeber**: doppelt verschachteltes Karten-Grid repariert, echte Bilder statt
  Logo-Platzhalter, alle Karten verlinkt, responsive 1/2/3-spaltig.
- **Aktuelle Angebote**: Karten auf Desktop exakt dreispaltig, gleiche Höhen.
- **Stadtteilseiten fertiggestellt**: Lindenthal, Sülz, Ehrenfeld, Nippes, Rodenkirchen mit
  individuellen Markt-Abschnitten (Preisniveau als redaktionelle Richtwerte), je zwei lokalen
  Eigentümer-Fragen und Querverlinkung der Veedel.


## Was in v5 umgesetzt wurde (Conversion & SEO)
- **Bewertungsformular auf der Startseite** (`js/bewertung.js`): alle Pflichtfelder inkl. PLZ mit
  automatischer Stadtteil-Erkennung (PLZ_MAP), stadtteilgenaue Marktrichtwerte, Bodenrichtwerte
  als BORIS.NRW-Struktur (manuell pflegbar, Funktion `lookupBodenrichtwert()` für spätere Anbindung).
  Ergebnis sofort als Spanne, Lead geht an sendmail.php.
- **Finanzierungsrechner**: Sollzins-Standard 4,5 %, Kaufpreis/Eigenkapital leer mit Platzhaltern,
  Rate mit dezentem Gold-Glow (`.rate-highlight`), neutrale Striche vor Eingabe.
- **Budget-Rechner**: Personen im Haushalt (Lebenshaltung 700 €/Person, automatisch vorgeschlagen),
  Haushaltsnettoeinkommen gesamt, Fixkosten als Gesamtbetrag, nachvollziehbare Rechen-Aufschlüsselung
  im Ergebnis, Sollzins 4,5 %.
- **Team**: 3 Karten nebeneinander, persönliche Vorstellung beim Hover (Touch: unter der Karte),
  Rolle „Immobilienmakler & Baufinanzierer".
- **Kontakt**: Bild eingebunden, Headline „Ich freue mich auf Ihre Anfrage.".
- **Hero**: dezente Licht-Animation (`.hero__glow`, respektiert prefers-reduced-motion).
- **Navigation**: gruppierte Hover-Dropdowns (Immobilie verkaufen / Finanzierung / Für Eigentümer /
  Über uns), Mobile-Menü mit Aufklapp-Gruppen — auf allen Seiten.
- **Newsletter-Sektion** mit DSGVO-Einwilligung und Double-Opt-in-Hinweis (Versand über sendmail.php;
  vor Livegang an Newsletter-Tool wie Brevo/Mailchimp anbinden).
- **Google-Bewertungen**: erfundene Beispiel-Rezensionen entfernt; `js/reviews.js` als pflegbare
  Struktur (rating/count/reviews[] mit echten Google-Rezensionen füllen, placeId für Bewertungslink),
  plus Bereich „Ihre Erfahrung ist uns wichtig".
- **Über-uns-Seite** (`ueber-uns.html`) mit Unternehmensprofil, Team, Kranhaus-Standort und CTAs.
- **SEO**: Meta-Titles/Descriptions mit Fokus-Keywords (Immobilienmakler Köln, Immobilienbewertung
  Köln kostenlos, Immobilie verkaufen Köln …), areaServed im Schema um Umland erweitert
  (Rhein-Erft-Kreis, Hürth, Frechen, Pulheim, Brühl, Wesseling, Leverkusen, Bergisch Gladbach),
  Umland-Absatz in der Standorte-Sektion, Sitemap ergänzt.

- **Unterseiten inhaltlich ausgebaut**: Baufinanzierung (Ablauf + FAQ), Käuferkartei (3-Schritte-Erklärung),
  Wissen (Ratgeber-Texte mit internen Links), Angebote (Kaufinteressenten-/Eigentümer-Sektion),
  Immobilienmakler Köln (Preis- und Umland-Texte, Platzhalter „in Vorbereitung" entfernt),
  Immobilie verkaufen (FAQ-Sektion). Ratgeber-Karten jetzt mehrspaltig.

## Vor dem Livegang zusätzlich zu pflegen (v5)
1. `js/reviews.js`: echte Google-Rezensionen, Gesamtwertung und placeId eintragen.
2. `js/bewertung.js` und `js/wertrechner.js`: Markt- und Bodenrichtwerte regelmäßig prüfen (BORIS.NRW).
3. Newsletter: Anbindung an ein Double-Opt-in-fähiges Tool statt sendmail.php.


## Was in v4 umgesetzt wurde (Redesign)
- **Foto-Hero** auf der Startseite (`assets/img/hero-koeln-abend.jpg`) statt Illustration; fehlerhafte SVG-Kranhaus-Grafik entfernt.
- **Neue Bildsprache**: 5 hochwertige Motive eingebunden (`hero-koeln-abend`, `bewertung-koelnblick`, `beratung-buero`, `wohntraum-wohnzimmer`, `expose-verkauf`).
- **Immobilienbewertungs-Sektion** prominent direkt unter dem Hero, mit klarer Headline und CTA.
- **Farbsystem beruhigt**: Navy + Weiß + dezentes Gold; grelles Blau und Buntheit reduziert.
- **Header luftiger**: mehr Höhe, klare Navigation, WhatsApp-Button aus dem Header entfernt.
- **Sterne einheitlich** als SVG (Gold), Trust-Leiste und Bewertungen korrigiert.
- **Awards entfernt**: Der frühere Abschnitt „Auszeichnungen“ wurde durch den seriösen Abschnitt „Qualifikationen & Vertrauen“ ersetzt (§ 34c/§ 34i GewO, unabhängige Baufinanzierung, persönlicher Ansprechpartner in Köln); unbelegte Award- und Bewertungssiegel sowie die Golf-Partner-Grafik entfernt.
- **Kontrast-Fixes**: Kontaktbereich auf dunklem Grund jetzt lesbar, Formular-Fokusfarben angepasst.
- **Widerrufsbelehrung** als eigene Seite (`widerruf.html`), im Footer aller Seiten verlinkt, Hinweis unter allen Formularen; Sitemap ergänzt.
- **Interne Notizen entfernt** (review-flags in Impressum/Datenschutz), Lade-Splashscreen entfernt.


Statische, schnelle Premium-Website (HTML/CSS/JS + ein PHP-Mailskript) für den
Kölner Makler- und Finanzierungsbetrieb **Highseller Immobilien & Finanzen**
(Inhaber Baris Ölmez, Kranhaus 1, Köln).

## Was in v3 umgesetzt wurde
- **Hausverwaltung vollständig entfernt** (Seite, Menü, Footer, Formular, Meta, Sitemap). Fokus: Verkauf, Bewertung, Vermittlung, Baufinanzierung, Finanzierungsberatung, Käuferprüfung, Eigentümerberatung.
- **Budget-Rechner** (`budget-rechner.html`, `js/budget.js`): Rückwärtsrechnung max. Kaufpreis, Variante A (Wunschrate) / B (Einnahmen − Ausgaben), Kaufnebenkosten inkl. Grunderwerbsteuer je Bundesland, Restschuld nach Zinsbindung, Einschätzung + Lead-Versand.
- **Teamfotos** (Baris, Serhad, Romeo) eingebunden; **Baris** zusätzlich im Hero, in der persönlichen Vorstellung und im Kontaktbereich.
- **Kölner Kranhäuser** als hochwertige stilisierte Illustration im Hero (Köln-Bezug, kein Stockfoto).
- **Header verschlankt**: flache 6-Punkt-Navigation, größeres Logo, Telefon **+49 162 8811110**, CTA „Kostenlos beraten lassen".
- **Trust-Leiste** direkt unter dem Hero (200+ Verkäufe · Bewertungen · Auszeichnungen · regionale Expertise · aus einer Hand).
- **Bewertungen & Auszeichnungen** weit oben auf der Startseite platziert.
- **Persönliche Vorstellung von Baris Ölmez** mit Foto, Text und CTA „Persönliches Beratungsgespräch anfragen".
- **200+ Verkäufe** als Vertrauenszahl im Hero und in der Trust-Leiste.
- Begriff **„Vertriebserfahrung" → „Verkaufserfahrung"**, Telefon überall **+49 162 8811110**.
- Alle Formulare → `sendmail.php` an **info@high-seller.de**, mit DSGVO-Checkbox und prominenter Danke-Meldung („Vielen Dank für Ihre Anfrage. Wir melden uns zeitnah persönlich bei Ihnen.").
- Design: mehr Weißraum, größere Bilder, dezente Goldakzente, hochwertige Schatten/Karten, mobil optimiert.

## Struktur
- `index.html` Startseite · `immobilie-verkaufen.html` · `immobilie-bewerten.html` (Wertrechner) · `baufinanzierung.html` · `baufinanzierungsrechner.html` · `budget-rechner.html` · `immobilien-angebote.html` · `kaeuferkartei.html` · `kontakt.html` · `faq.html` · `wissen.html` · Stadtteilseiten + `immobilienmakler-koeln.html` · `impressum.html` · `datenschutz.html`
- `css/styles.css` · `js/main.js`, `js/wertrechner.js`, `js/budget.js`, `js/calculator.js`
- `assets/img/` (Fotos, Logo, Siegel, Favicons) · `sendmail.php` · `sitemap.xml` · `robots.txt`

## Vor dem Live-Gang noch zu erledigen
1. **`sendmail.php`**: `$ABSENDER` auf eine real existierende Postfach-Adresse setzen; für zuverlässigen Versand SMTP/PHPMailer nutzen (Hinweis im Skript). PHP-Hosting erforderlich.
2. **Echte Immobilienfotos** einsetzen: Objekt-/Stadtbilder sind aktuell dezent gebrandete Flächen (Logo auf Navy). Sobald lizenzierte Fotos vorliegen, die `.img-brand`-Flächen ersetzen.
3. **Bewertungen** auf der Startseite sind Beispieltexte — vor Launch durch echte Google-Bewertungen ersetzen (oder Google-Widget einbinden).
4. **Beispiel-Angebote** (3 Listings) durch echte Objekte ersetzen bzw. an Portal-/IDX-Feed anbinden.
5. **Wertrechner-Richtwerte** (€/m², Bodenrichtwerte in `js/wertrechner.js`) und **Grunderwerbsteuer** (`js/budget.js`) regelmäßig prüfen/pflegen.
6. **Impressum & Datenschutz** rechtlich gegenprüfen lassen.

## Bewusst nicht enthalten
Kein Backend/CRM, keine bezahlten Marktdaten, keine Google-Places-Autocomplete. Leads kommen per E-Mail (bzw. mailto-Fallback) an. Diese Bausteine können als Folgeschritt ergänzt werden.
