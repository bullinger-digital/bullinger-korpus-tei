# Dokumentation zur Mithelfen-Kampagne

**Personen- und Ortsnamen** stellen einen interessanten Zugang zum Briefwechsel dar, nicht zuletzt über die Verlinkung mit anderen Wissensressourcen und Projekten.

Basierend auf den Personen- und Ortsregistern der HBBW-Edition haben wir die entsprechenden Eigennamen mittels NER (Name Entity Recognition) in den edierten Briefen (d.h. Brieftexte, Regesten und Fussnoten) ausgezeichnet und nach Möglichkeit mit dem jeweiligen Eintrag in unserem Register verknüpft. Dabei haben wir auch die verschiedenen Schreibvarianten der Namen in unser Register aufgenommen. Unsere Registereinträge haben wir nach Möglichkeit automatisch mit einer externen Wissensressource (Wikipedia, GND, HLS, Geonames) verknüpft und versucht, daraus weitere Schreibvarianten des Names zu gewinnen.

Basierend auf diesen Daten haben wir in einem zweiten Schritt die Eigennamen in den manuell transkribierten Briefen markiert.

Schliesslich haben wir durch eine Citizen Science Kampagne (Mithelfen-Kampagne) die automatischen Markierungen und Verknüpfungen manuell kontrollieren und fehlende Markierungen ergänzen lassen. Dabei wurden alle vorgelegten Briefe (8'591 an der Zahl) mindestens 1x aufgerufen und 4'818 Briefe (56%) vollständig kontrolliert. 

Zusammen mit den Freiwilligen haben wir 6'014 verschiedene Personen und 3'083 Ortschaften in den Briefen gefunden und 184'047 Personen- und 147'378 Ortsmarkierungen vorgenommen. Dabei konnten wir 2398 Personen mit einem GND-Eintrag verlinken.

Für die Mithelfen-Kampagne haben wir folgende Annotationsrichtlinien definiert:

## Namensschreibung

- In der Schreibung orientieren wir uns an den externen Wissensressourcen; 
- relevante Varianten (z.B. latinisierte Version des Namens) geben wir als Alias an;
- Namenszusätze setzen wir in runde Klammern, z.B. Friedrich II. (der Sanftmütige);
- sofern bekannt, geben wir bei Frauen den Geburts- und Ehenamen an und kennzeichnen diese mit geb. (geboren), verh. (verheiratet) und verw. (verwitwet);
- Ergänzungen (z.B. zur Unterscheidung gleichnamiger Personen) geben wir in runden Klammern an, z.B. _Heinrich Bullinger (Reformator), Heinrich Bullinger (Vater des Reformators),	Heinrich Bullinger (Vetter des Reformators), Heinrich Bullinger d.J. (Sohn des Reformators)_

## Personen 

1.	Wir markieren alle Personennamen für historische Personen. Beispiele: 
    - Vornamen + Nachnamen; z.B. _Iodocus Kilchmeyerus, Johann Jakob Simler, Gerhardus zum Camph_
    - nur Nachnamen, z.B. _Gessner, Bibliander_
    - nur Vornamen, z.B. _Theodorus, Leonie_
2.	Titel, die vor oder hinter Personennamen stehen, markieren wir nicht, z.B. _Herzog Ulrich von Wirtemberg, Christophorus, dux Bavariae Palatinus_, ausser wenn sie zur Identifikation eines alleinstehenden Namens dienen, z.B. _Herzog Moritz, rex Ferdinandus_.
3.	Titel, die vor oder hinter Ländernamen stehen, markieren wir zusammen mit dem Ländernamen als Person, z.B. _rex Galliae_, und weisen die Person nach Möglichkeit dem entsprechenden Registereintrag zu.
4.	Bei Personennamen, die einen Ortsnamen enthalten, markieren wir den Personennamen einschliesslich des Ortsnamens, z.B. _Eberhard von Rümlang_.
5.	Ein nachgestellter Ortsname ist nicht Bestandteil des Personennamens und wird getrennt markiert, z.B. _Osvaldo Myconio, Basiliensis; Iohannes Burcherus Anglus_.
6.	Ein Ländername, der eindeutig den Regenten bezeichnet, wird als Personennamen markiert, z.B. _Danus_ für den König von Dänemark.

### Sonderfälle
1.	Die alleinstehenden Titel _Kaiser, Papst und Sultan_ weisen wir der Person zu, die zum jeweiligen Zeitpunkt dieses Amt innehatte.
2.	In Latein kommen gelegentlich Personennamen mit einem eingeschobenen Pronomen vor, z.B. _Gervasius tuus Schuler_. In diesen Fällen markieren wir den Personennamen einschliesslich des Pronomens.
3.	In Latein kommen gelegentlich Personennamen mit der angehängten Konjunktion -que (= und) vor. In diesen Fällen markieren wir den Personennamen einschliesslich der Konjunktion.
4.	Volksstämme, die sich nicht einem bestimmten Land zuordnen lassen, z.B. _Alemannen_, markieren wir und ergänzen den Eintrag mit (_Volk_).

### Ausnahmen: Wir markieren **nicht**
1.	Personen, die Kirchen oder Pfarreien bezeichnen, z.B. _Pfarrer zu St. Martin_;
2.	Personen, die Kalendertage bezeichnen, z.B. _am Tag nach Martini_;
3.	Personen der Bibel, z.B. _Moses, Jesus Christus, Satan / Belial, Gott / Deus_;
4.	Götter, z.B. _Mars_;
5.	Sagengestalten, z.B. _Musen_;
6.	Personengruppen im Sinne von "Anhänger einer Person", z.B. _Lutheraner, Zwinglianer_;
7.	alleinstehende Titel oder Funktionen, die nicht eindeutig sind, z.B. _Landgraf_;
8.	Personen in Sekundärliteratur-Angaben in den Fussnoten (z.B. Autorennamen, Personennamen in Buchtiteln).

## Ortsnamen 
1.	Wir markieren alle geographischen Namen der folgenden Toponym-Klassen: 
    - Städtenamen (eingliedrig oder mehrgliedrig), z.B.  _Bern, Augsburg, London, Augustae Vindelicorum, Stein am Rhein_; 
    - Ländernamen, z.B. _England, Dänemark_;
    - Gebietsnamen, z.B. _Breisgau, Unterwalden, Valle Tellina_;
    - Flussnamen. z.B. _Aare, Donau, Lech, Rhein_;
    - Seenamen, z.B. _Bodensee_.
2.	Die Einwohner einer Stadt oder eines Landes werden als Ortsname markiert, z.B. Frantzhosen, Italianer, Schweden, Teutschen, da sie häufig nicht von Orts-Adjektiven zu unterscheiden sind, z.B. _Germania, Teutschen_.
3.	Die in den Briefen erwähnten Eidgenossen markieren wir als Ortsname Schweiz.
4.	Gebietsnamen, die einen Zusammenschluss bezeichnen, werden markiert, wenn sie  
    - aus einer Zahl und einem Substantiv bestehen, z.B. _3 Pündt, 5 Orten, 4 Urbes, 5 Pagos, 7 Cantones_;
    - aus einem Zahlwort mit Substantiv bestehen, z.B. _Duorum Foederum, Trium Foederum, Zween Pündt, Fünff Orten_;
    - ein Herrschaftsgebiet umfassen, z.B. _Bavariae Palatinus_.
5.	Gebietsbezeichnungen, die in dieser Form heute nicht mehr existieren, sollten dem Ort / der Region zugewiesen werden, unter dem / der sie am einfachsten zu finden sind, z.B. Kanton Appenzell (vor der Aufteilung in Halbkantone) zuweisen zu Ort _Appenzell_.
6.	Gebietsbezeichnungen, die Ähnlichkeiten zu aktuellen Bezeichnungen haben, werden dieser zugeordnet. Häufige Beispiele dazu sind:
    - _Germanie inferioris_ zu Niederlande
    - _Germanie superiore_ zu Süddeutschland
    - _Frysia Orientalis_ zu Ostfriesland

### Ausnahmen: Wir markieren **nicht**
1.	Orte in Sekundärliteratur-Angaben in den Fussnoten, z.B. Ortsnamen in Buchtiteln, Verlagsort;
2.	Standort des Archivs, z.B. _StAZH Zürich_;
3.	Ländernamen, die zur Bezeichnung einer Sprache verwendet werden, z.B. _im Deutschen_;
4.	Ländernamen, die als Adjektiv verwendet werden, z.B. _deutsche Sprache_. Als Faustregel gilt: kleingeschriebene Ländernamen markieren wird nicht.
