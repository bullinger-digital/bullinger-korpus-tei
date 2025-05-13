# Bullinger Digital (Korpus in TEI-XML)

Bullinger Digital war von 2020-2025 ein am Institut für Computerlinguistik der Universität Zürich angesiedeltes Projekt mit dem Ziel, den 12'000 Briefe umfassenden Briefwechsel des Zürcher Reformators Heinrich Bullinger (1504-1575) online verfügbar zu machen. Das Projekt war in zwei Phasen aufgeteilt: In der ersten Phase haben wir eine Datenbank über alle Briefe aufgebaut und ein eigenes Online-Suchsystem entwickelt (s. https://github.com/bullinger-digital/bullinger-korpus). In der zweiten Phase haben wir die Daten in das vorliegende Korpus in TEI-XML überführt, um die langfristige Verfügbarkeit und weitere Bewirtschaftung der Daten zu gewährleisten. Per Projektende im Mai 2025 wurde dieses Korpus ans Staatsarchiv des Kantons Zürich übergeben, welches bereits den Grossteil der überlieferten Briefe aufbewahrt und nun auch die langfristige Pflege des Online-Suchsystems unter www.bullinger-digital.ch übernimmt. Das vorliegende Korpus gibt den Stand per Projektabschluss Ende Mai wieder.

Folgende Arbeiten liegen dem Bullinger Digital Korpus zugrunde, sie sind unter https://github.com/bullinger-digital/bullinger-korpus-tei/tree/main/docs ausführlicher beschrieben:

- Zusammenstellung der verfügbaren Informationen pro Brief
    - Metadaten wie Absender/Empfänger, Briefdatum, Aufbewahrungsort und Signatur des Manuskripts etc. (aus der gedruckten HBBW-Edition, aus den Karteikarten des HBBW-Editionsteams)
    - Regesten (aus der gedruckten HBBW-Edition)
    - Kommentarapparat als Fussnoten (aus der gedruckten HBBW-Edition)
    - Brieftexte (aus der gedruckten HBBW-Edition, aus anderen gedruckten Editionen, aus den Vorarbeiten des HBBW-Editionsteams, automatisch erstellte Transkriptionen)
    - Faksimile der Briefe (hauptsächlich vom Staatsarchiv des Kantons Zürich und der Zentralbibliothek Zürich)
- Spracherkennung und Auszeichnung des Sprachwechsels in den Brieftexten
- Normalisierung der frühneuhochdeutschen Brieftexte zur Vereinfachung der Online-Suche
- automatische Übersetzung der Regesten und Brieftexte auf Englisch
- automatische Handschriftenerkennung für Briefe ohne Transkription und mit Faksimile 
- automatische Verschlagwortung
- Named Entity Recognition und Entity Linking mit anschliessender manueller Korrektur mittels Citizen Science-Kampagne 

### Impressum

Folgende Personen haben an der Erstellung des Bullinger-Korpus mitgewirkt:

- Projektleitung: Patricia Scheurer, Phillip B. Ströbel, Martin Volk
- Technische Umsetzung: Raphael Müller, Bernard Schroffenegger
- Korpus-Aufbereitung und Annotation: Lukas Fischer, Dominic P. Fischer, Anastassia Shaitarova
- Linguistische Beratung und Annotation: Raphael Schwitter
- Abstimmung mit der HBBW-Edition am IRG der UZH: Tobias Jammerthal, David Mache, Paul Neuendorf, Peter Opitz, Judith Steiniger
- Recherchen und Annotation: Peter Rechsteiner
- Bibliothekarische und archivarische Koordination: Jesko Reiling (ZB Zürich), Christian Sieber (Staatsarchiv Zürich)
- Automatische Handschriften-Erkennung: Andreas Fischer und Team an der Hochschule Fribourg, Tobias Hodel und Team an der Universität Bern
- Technische und administrative Unterstützung: Eyal Dolev, Leo Rutschmann, Elainne Vibal
- Studentische Mitarbeitende: Donn Edvard Anin, Sabrina Brändle, Nikolaj Bauer, Isabelle Cretton, Angela Heldstab, Jana-Maria Humbel, Diana Merkle, Maria Christina Panagiotopoulou, Antonia Popp, Ismail Prada, Benjamin Suter
- Finanzielle Förderung: UZH Foundation
- Kontakt: bullinger-digital@protonmail.com

### Zitiervorschlag

```
Patricia Scheurer and Raphael M{\"u}ller and Bernard Schroffenegger and Phillip B. Str{\"o}bel and Martin Volk (2025): Bullinger Digital Briefkorpus. Briefe von und an Heinrich Bullinger 1523 bis 1575.
Universität Zürich, Institut für Computerlinguistik, https://github.com/bullinger-digital/bullinger-korpus-tei.

@misc{Scheurer_et_al_2025,
	author = {Patricia Scheurer and Raphael M{\"u}ller and Bernard Schroffenegger and Phillip B. Str{\"o}bel and Martin Volk},
	howpublished = {Digitale Edition},
	month = {Mai},
	title = {Bullinger Digital Briefkorpus. Briefe von und an Heinrich Bullinger 1523 bis 1575},
	year = {2025},
	school = {Universität Zürich, Institut für Computerlinguistik},
	url = {https://github.com/bullinger-digital/bullinger-korpus-tei}}
```

### Weiterführende Informationen

- HBBW-Edition: https://www.irg.uzh.ch/de/forschung/bullinger/edition-briefwechsel.html
- Bullinger Digital Projekt: https://www.cl.uzh.ch/de/research-groups/texttechnologies/research/digital-humanities/bullinger.html
- Publikationsliste: https://www.cl.uzh.ch/de/research-groups/texttechnologies/research/digital-humanities/bullinger.html
- Online-Suchsystem: www.bullinger-digital.ch
- TEI-Publisher für digitale Editionen: https://www.e-editiones.org/

### Urheberrecht

Das Projekt Bullinger Digital ist der Open-Science-Policy und den FAIR-Prinzipien verpflichtet. Texte sind unter Creative Commons BY-NC-ND 3.0 CH lizenziert und können unter Angabe des Urhebers (s. Zitiervorschlag) und einem Link zur Lizenz für wissenschaftliche, private und nicht-kommerzielle Zwecke vervielfältigt und weiterverbreitet werden.
Die Faksimiles sind unter Creative Commons BY-SA 4.0 lizenziert und können unter Angabe des Urhebers (= Ort der Aufbewahrung und Signatur; gemäss Quellenangabe oberhalb des Digitalisats) und einem Link zur Lizenz für wissenschaftliche, private, nicht-kommerzielle und kommerzielle Zwecke frei verwendet werden. Bei den Faksimiles ist zusätzlich die Signatur anzugeben. 

