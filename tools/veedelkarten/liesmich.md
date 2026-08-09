# Grafiken der Veedelseiten

Beide Skripte erzeugen Inline-SVG, das anschließend von Hand in die jeweilige
Seite übernommen wird. Sie laufen ohne Fremdbibliotheken.

    python3 tools/veedelkarten/karte-deutz-bauen.py
    python3 tools/veedelkarten/preisdiagramm-bauen.py

## karte-deutz-bauen.py

Projiziert die Umrisse aus `rohdaten/` in eine Zeichenfläche und setzt die
Landmarken an ihre echten Koordinaten. Die erste, frei gezeichnete Fassung der
Karte war an mehreren Stellen schlicht falsch: Die Köln Arcaden lagen mittig
statt im Osten, Hyatt und KölnTriangle untereinander statt nebeneinander, und
die Poller Wiesen standen als Deutzer Grünfläche darin, obwohl sie in Poll
liegen. **Deshalb nichts mehr nach Augenmaß setzen, sondern Koordinaten
nachschlagen.**

Der Kartenausschnitt ist bewusst fest gesetzt und zeigt nicht die ganze
Stadtteilfläche: Deutz reicht im Süden weit über den Hafen hinaus, alle
Landmarken lägen dann gedrängt im oberen Fünftel.

Die Beschriftungsrichtung je Landmarke steht von Hand im Skript. Eine
automatische Regel kollidiert bei dieser Dichte immer irgendwo.

## preisdiagramm-bauen.py

Liest `src/data/stadtteile-marktdaten.json` und erzeugt zwei Fassungen: die
volle mit allen zwanzig Stadtteilen für breite Bildschirme und eine
fokussierte mit sieben Zeilen fürs Handy. Dort wären zwanzig Zeilen nur mit
seitlichem Scrollen lesbar — und abgeschnitten würde ausgerechnet die
Wertespalte, sodass alle Balken gleich lang aussähen.

## rohdaten/

Auszug aus OpenStreetMap über die Overpass-API, gefiltert auf das, was die
Karte braucht. Die Daten liegen hier, weil die Overpass-API bei größeren
Abfragen regelmäßig in Zeitüberschreitungen und Ratenbegrenzungen läuft; ein
Neuaufbau der Karte soll davon nicht abhängen.

Lizenz der Umrisse: OpenStreetMap-Mitwirkende, ODbL. Die Nennung steht in der
Karte selbst und in der Bildunterschrift auf der Seite.
