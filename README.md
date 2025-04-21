# Bullinger Digital (Korpus in TEI-XML)

Heinrich Bullinger (1504-1575) war ein Mitarbeiter und Nachfolger von Huldrich Zwingli und ein wichtiger Multiplikator
für die Ideen der Reformation in der Schweiz und in Europa. Von seiner umfangreichen Korrespondenz sind 12'000 Briefe
erhalten; davon hat er rund 10'000 Briefe empfangen, etwa 2'000 Bullinger selbst geschrieben. Die meisten Originale
werden im Staatsarchiv Zürich und in der Zentralbibliothek Zürich aufbewahrt. 80% der Briefe sind in lateinischer
Sprache, die meisten anderen in Frühneuhochdeutsch. Basis für das Projekt Bullinger Digital waren die vom Institut für
Schweizerische Reformationsgeschichte (IRG) erarbeiteten Daten. Diese umfassen die Metadaten zum gesamten Briefwechsel,
3'100 bereits edierte Briefe sowie provisorische Transkriptionen zu weiteren 5'400 Briefen. 

### Projektziele

#### Bullinger Digital \[1.0\] (Januar 2021 bis Mai 2023)

Bullinger Digital hatte das Ziel, den gesamten Briefwechsel online verfügbar zu machen. In einem ersten Schritt wurden
die auf Karteikarten vorhandenen Metadaten digitalisiert und mithilfe der interessierten Öffentlichkeit (Citizen
Science-Kampagne) in eine Datenbank überführt. In einem zweiten Schritt haben wir die Datenbank um die vorhandenen
Brieftexte, die wissenschaftlichen Kommentare aus der HBBW-Edition und die eigens für das Projekt erstellten
Digitalisate der Briefe ergänzt. Zudem haben wir auf der Basis der Scan-alignierten Transkriptionen Systeme zur
Handschrifterkennung (HTR) trainiert, um die restlichen 3'500 Briefe effizient in elektronischen Text umzuwandeln.
Auch haben wir ein System zur maschinelle Übersetzung erstellt, das die in mittelalterlichem Latein geschriebenen Briefe
in modernes Deutsch übersetzt, sowie ein Modell zur Normalisierung der in Frühneuhochdeutsch geschriebenen Briefe
entwickelt. Das Ergebnis dieser Arbeiten steht unter www.bullinger-digital.ch der Forschungsgemeinschaft und der
interessierten Öffentlichkeit zur Verfügung.

Technische Tools:

- Datenbank/Suchsystem: SQLite, Python, Cantaloupe IIIF-Server, Elasticsearch, React (NextJS)
- Automatische Handschriftenerkennung: HTR-Flor, Transkribus, TrOCR
- Automatische Zeichenerkennung (OCR): ABBYY-FineReader
- Maschinelle Übersetzung: Sockeye, Classical Language Toolkit
- Selbst entwickelte Programme zur Sprachidentifikation (Latein vs. Frühneuhochdeutsch) und Erkennung von Code-Switching
- XML-Editor Oxygen
- GitHub für Versionskontrolle und Download
- Trello für Fehlermeldungen

Unterstützt durch Zuwendungen an die UZH Foundation von:

- Baugarten Stiftung (https://www.baugarten-zuerich.ch/)
- Ernst Göhner Stiftung (http://www.ernst-goehner-stiftung.ch/)
- Hasler Stiftung (https://haslerstiftung.ch/)
- Otto Gamma Stiftung
- Ref. Kirche Kanton ZH (https://www.zhref.ch/)
- Ref. Kirche Stadt ZH (https://www.reformiert-zuerich.ch/)
- Stiftung Symphasis/Accentus (https://www.symphasis.ch/)
- Partizipative Wissenschaftsakademie (https://www.pwa.uzh.ch/de.html)
- Christian Rahn
- Hans und Margrit Neukom

#### Bullinger Digital 2.0 (Januar 2024 bis Juni 2025)

Im Folgeprojekt Bullinger Digital 2.0 wollen wir Bullinger Digital in den TEI-Publisher überführen, um die langfristige
Verfügbarkeit des Online-Zugriffs zu garantieren, das Korpus um automatische Verschlagwortung anreichern, die
automatische Eigennamenerkennung (NER) weiter verbessern und in einer weiteren Citizen Science-Kampagne
kontrollieren/korrigieren lassen. Auch die Vernetzung des Briefwechsels mit anderen Wissensressourcen und
Editionsprojekten soll weiter ausgebaut werden.

Unterstützt durch Zuwendungen an die UZH Foundation von:

- Baugarten Stiftung (https://www.baugarten-zuerich.ch/)
- Ernst Göhner Stiftung (http://www.ernst-goehner-stiftung.ch/)
- Goethe-Stiftung für Kunst und Wissenschaft
- Kostermann-Stiftung
- Otto Gamma Stiftung
- Ref. Kirche Graubünden
- Ref. Kirche Kanton ZH (https://www.zhref.ch/)
- Ref. Kirche St. Gallen

### Impressum

#### Projektteam

Institut für Computerlinguistik, Universität Zürich (Andreasstrasse 15, 8050 Zürich):

- Prof. Dr. Martin Volk (Projektverantwortlicher)
- Dr. Patricia Scheurer (Administration)
- Dr. Anastassia Shaitarova (automatische Verschlagwortung)
- Raphael Müller (Front-/Back-End-Entwicklung)
- Bernard Schroffenegger (Daten/Back-End-Entwicklung)
- Dr. Phillip B. Ströbel (HTR)
- PD Dr. Raphael Schwitter (Lateinische Philologie)

In Zusammenarbeit mit

- Prof. Dr. Andreas Fischer (Hochschule für Technik und Architektur Freiburg)
- Prof. Dr. Tobias Hodel (Universtität Bern)
- Prof. em. Dr. Peter Opitz (Institut für Schweizerische Reformationsgeschichte)
- Prof. Dr. Tobias Jammerthal (Institut für Schweizerische Reformationsgeschichte)
- Dr. Paul A. Neuendorf (Institut für Schweizerische Reformationsgeschichte)
- David Mache (Institut für Schweizerische Reformationsgeschichte)
- Christian Sieber (Staatsarchiv des Kantons Zürich)
- Dr. Anna Scius-Bertrand (Hochschule für Technik und Architektur Freiburg)
- Dr. Stefan Wiederkehr (Zentralbibliothek Zürich)
- PD Dr. Jesko Reiling (Zentralbibliothek Zürich)
- Laura Furlanetto (UZH Foundation)

Studentische Mitarbeitende:

Dominic Fischer, Jana-Maria Humbel, Eyal Dolev, Angela Heldstab, Anna Mogillo, Antonia Popp, Ismail Prada,
Benjamin Suter, Elainne Marie Vibal

Herzlichen Dank an alle Freiwilligen:

- Bürgerkomitee
- Beteiligte an der Citizen Science-Kampagne
- Peter Rechsteiner

#### Zitiervorschlag

Institut für Computerlinguistik und Institut für Schweizerische Reformationsgeschichte der Universität Zürich (Hrsg.):
Bullinger Digital. Digitale Erschliessung von Heinrich Bullingers Briefwechsel. 2020-2025. www.bullinger-digital.ch.
Zugriff am DD.MM.YYYY.

@misc{BullingerDigital2020,
title = {Bullinger {Digital}},
copyright = {Institut für Computerlinguistik und Institut für Schweizerische Reformationsgeschichte der Universität Zürich},
url = {https://www.bullinger-digital.ch},
urldate = {YYYY-MM-DD},
year = {2025},
}

#### Haftungsausschluss bei eigenen Inhalten

Eine Haftung für die Richtigkeit, Vollständigkeit oder Aktualität dieser Webseiten und jederzeitige Verfügbarkeit der
bereitgestellten Informationen wird abgelehnt. Das Institut für Computerlinguistik der Universität Zürich übernimmt
keinerlei Haftung für eventuelle Schäden oder Konsequenzen, die durch die direkte oder indirekte Nutzung der angebotenen
Inhalte entstehen. Für etwaige Schäden, die beim Aufrufen oder Herunterladen von Daten durch Computerviren oder der
Installation oder Nutzung von Software verursacht werden, wird nicht gehaftet.

#### Haftungsausschluss bei Querverweisen und Links

Die Inhalte fremder Seiten, auf die von www.bullinger-ditigal.ch mittels Links hingewiesen wird, dienen lediglich der
Information und der Darstellung von Zusammenhängen. Für illegale, fehlerhafte oder unvollständige Inhalte und
insbesondere für Schäden, die aus der Nutzung verlinkter Informationen entstehen, wird vom Institut für
Computerlinguistik der Universität Zürich jede Haftung abgelehnt.

#### Urheberrecht

Das Projekt Bullinger Digital ist der Open-Science-Policy und den FAIR-Prinzipien verpflichtet. Texte sind unter
Creative Commons BY-NC-ND 3.0 CH lizenziert und können unter Angabe des Urhebers (s. Zitiervorschlag) und einem Link zur
Lizenz für wissenschaftliche, private und nicht-kommerzielle Zwecke vervielfältigt und weiterverbreitet werden.
Die Faksimiles sind unter Creative Commons BY-SA 4.0 lizenziert und können unter Angabe des Urhebers (= Ort der
Aufbewahrung und Signatur; gemäss Quellenangabe oberhalb des Digitalisats) und einem Link zur Lizenz für
wissenschaftliche, private, nicht-kommerzielle und kommerzielle Zwecke frei verwendet werden. Bei den Faksimiles ist
zusätzlich die Signatur anzugeben; diese ist oberhalb der Bildansicht ausgewiesen. 

### Publikationen und Referate

#### Spezielle Veranstaltungen

- 12.5.2025: Öffentliche Veranstaltung zum Projektabschluss
- 1.6.2024: Öffentlicher Workshop in der Zentralbibliothek Zürich zum Auftakt der Citizen Science Kampagne Bullinger-Briefwechsel
- 24.2.2023: Öffentliche Tagung zu «Bullinger Digital: 500 Jahre Bullingerbriefwechsel»
- 3.11.2021: Öffentliche Vorstellung des Projektes Bullinger Digital in der Zentralbibliothek Zürich

#### Forschungsbeiträge

- Ströbel, P.B., Fischer, L., Müller, R., Scheurer, P., Schroffenegger, B., Suter, B. and Volk, M. (2024): Multilingual Workflows in Bullinger Digital: Data Curation for Latin and Early New High German. In: Journal of Open Humanities Data, 10(1), p. 12.
- Stüssi, Elina; Phillip Ströbel (2024): Part-of-Speech Tagging of 16th-Century Latin with GPT.In: Proceedings of the 8th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2024).
- Volk, Martin; Fischer, Dominic Philipp; Fischer, Lukas; Scheurer, Patricia; Ströbel, Phillip (2024): LLM-based Machine Translation and Summarization for Latin. In: Third Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA 2024).
- Volk, Martin; Fischer, Dominic P; Scheurer, Patricia; Schwitter, Raphael; Ströbel, Phillip (2024): LLM-based Translation Across 500 Years. The Case for Early New High German. In: 20th Conference on Natural Language Processing (KONVENS 2024), Wien, Österreich, 10 September 2024 - 13 September 2024. Association for Computational Linguistics, 368-375.
- Scheurer, Patricia; Müller, Raphael; Schroffenegger, Bernard; Ströbel, Phillip; Suter, Benjamin; Volk, Martin (2023): Ein Briefwechsel-Korpus des 16. Jahrhunderts in Frühneuhochdeutsch. In: Neue Entwicklungen in der Korpuslandschaft der Germanistik. Beiträge zur IDS-Methodenmesse 2022, S. 33-42.
- Scius-Bertrand, Anna; Stroebel, Phillip; Volk, Martin; Hodel, Tobias, Fischer, Andreas (2023): The Bullinger Dataset: A Writer Adaptation Challenge. In: Proc. 17th Int. Conf. on Document Analysis and Recognition (ICDAR 2023).
- Ströbel, Phillip; Boente, Walter; Hodel, Tobias; Volk, Martin (2023):  The Adaptability of a Transformer-Based OCR Model for Historical Documents. In: Coustaty, M., Fornés, A. (eds) Document Analysis and Recognition – ICDAR 2023 Workshops. ICDAR 2023. Lecture Notes in Computer Science, vol 14193. Springer, Cham.
- Ströbel, Phillip; Hodel, Tobias; Fischer, Andreas; Scius, Anna; Wolf, Beat; Janka, Anna; Widmer, Jonas; Scheurer, Patricia; Volk, Martin (2023):  Bullingers Briefwechsel zugänglich machen: Stand der Handschriftenerkennung. In: Trilcke, Peer; Busch, Anna; Helling, Patrick (eds.) Open Humanities Open Culture. 9. Tagung des Verbands "Digital Humanities im deutschsprachigen Raum" (DHd 2023).
- Ströbel, Phillip; Scheurer, Patricia; Volk, Martin (2023): Lessons Learnt from Bullinger Digital. In: Open Up Digital Editions Conference 2024, Zurich, 24 Januar 2024 - 26 Januar 2024. Center Digital Editions & Edition Analytics (University Library Zurich) and Research and Infrastructure Support RISE (University of Basel), 75-76.
- Volk, Martin; Fischer, Lukas; Scheurer, Patricia; Schwitter, Raphael; Ströbel, Phillip (2023): Code-Switching: Profiling and Classifying the Language Mix in a Large Corpus of 16th Century Letters. Für: Proceedings of the Days of Computational Approaches to Ancient Greek and Latin. 
- Fischer, Lukas; Scheurer, Patricia; Schwitter, Raphael; Volk, Martin (2022): Machine Translation of 16th Century Letters from Latin to German. In: Second Workshop on Language Technologies for Historical and Ancient Languages (LT4HALA 2022), LREC 2022, S. 43-50.
- Spoto, Martin; Fischer, Andreas; Scius-Bertrand, Anna; Wolf, Beat (2022): Improving Handwriting Recognition for Historical Documents Using Synthetic Text Lines. In: Carmona-Duarte, C., Diaz, M., Ferrer, M.A., Morales, A. (eds): Intertwining Graphonomics with Human Movements. IGS 2022. Lecture Notes in Computer Science, vol 13424. Springer, Cham.
- Ströbel, Phillip; Clematide, Simon; Hodel, Tobias; Schoch, David; Schwitter, Raphael; Volk, Martin (2022): Evaluation of HTR models without Ground Truth Material. In: Proceedings of LREC 2022, European Language Resources Association.
- Volk, Martin; Fischer, Lukas; Scheurer, Patricia; Schwitter, Raphael; Ströbel, Phillip; Suter, Benjamin (2022): Nunc profana tractemus. Detecting Code-Switching in a Large Corpus of 16th Century Letters. In: Proceedings of LREC-2022, European Language Resources Association.

#### Referate

- 12.03.205: Vortrag LLMs bei Bullinger Digital von Dominic Fischer und Martin Volk am DIZH-Workshop Quellenanalyse nach dem ChatGPT-Schock.
- 28.11.2024: Vortrag Code-Switching: Profiling and Classifying the Language Mix in 16th-Century Letters von Martin Volk am ERASMOS workshop an der KU Leuven.
- 4.10.2024 + 18.10.2024: Co-Teaching von Patricia Scheurer und David Neuhold an der Theologischen Fakultät der Universität Luzern im Rahmen des Kurses Quellenstudium – Briefquellen allgemein, mit besonderer Berücksichtigung der digitalen Bullinger-Quellenedition von «Bullinger digital»
- 28.02.2024: Vortrag LLMs für Bullinger Digital von Dominik Fischer am Workshop W8a: Generative KI, LLMs und GPT bei digitalen Editionen zur DHd2024.
- 7.2.2023: Referat Bullinger Digital - Texterkennung in einem reformatorischen Briefwechselkorpus von Phillip Ströbel am Workshop CAIDAS: Data Analytics for Digital Humanities: Projects, Methods, Insights - Universität Würzburg.
- 13.3.2023: Gastvortrag zu Bullinger Digital am Moore Theological College in Sydney.
- 15.3.2023: Referat Nunc profana tractemus. Detecting Code-Switching in a Large Corpus of 16th Century Letters von Lukas Fischer am Workshop Days of Computational Approaches to Ancient Greek and Latin.
- 16.3.2023: Referat Bullingers Briefwechsel zugänglich machen: Stand der Handschriftenerkennung von Phillip Ströbel an der Konferenz DHd 2023.
- 13.4.2023: Referat Non quidem per omnia redditum - Reformatorischer Anspruch und translatorische Praxis in der Publizistik Heinrich Bullingers (1504-1575) von Raphael Schwitter an der Tagung The Wrong Direction - Frühneuzeitliche Übersetzungen ins Lateinische.
- 15.5.2023: Präsentation des Projekts Bullinger Digital von Patricia Scheurer anlässlich der Generalversammlung der Baugarten Stiftung.
- 2.-3.9.2023: Vertretung am Scientifica-Stand Historische Quellen Digital: Neue Zugänge zu altem Wissen.
- 15.11.2023: Vortrag Visualizing History von Martin Volk anlässlich der Vorlesungsreihe Thinking (About) Machines an der UZH.
- 9.2.2022: Referat Künstliche Intelligenz für Digitale Editionen von Martin Volk am Workshop Möglichkeiten computergestützter Auswertung von historischen Korrespondenzen.
- 16.3.2022: Breakout Room zu Ein Briefwechsel-Korpus des 16. Jahrhunderts in Frühneuhochdeutsch von Patricia Scheurer an der Methodenmesse Korpora in der germanistischen Sprachwissenschaft – mündlich, schriftlich, multimedial anlässlich der 58. Jahrestagung des Leibniz-Instituts für Deutsche Sprache.
- 8.6.2022: Breakout Room zu Bullinger Digital von Martin Volk an der Trilateral UZH – HUJI – FUB Online Science Fair on Digital Humanities.
- 29.6. bis 1.7.2022: Messestand zu Bullinger Digital an der «Swiss Landscape of Digital History» in Genf.
- 18.10.2022: Referat Bullinger Digital – From Scans, TUSTEP, PDFs, HTMLs and Text Files to TEI and an Online Search System von Phillip Ströbel an der Konferenz Digital Publishing for the Humanities: New Technologies and Ideas.
- 20.10.2022: Referat Bullinger Digital: the Transformation and Extension of an Analogue Edition into the Digital Age von Phillip Ströbel am DARIAH-CH Study Day.
- 25.10.2022: Präsentation des Bullinger Digital-Projektes von Martin Volk anlässlich einer Veranstaltung der UZH Foundation für die Zürcher Zünfte.
- 3.11.2021: Öffentliche Vorstellung des Projektes Bullinger Digital in der Zentralbibliothek Zürich.

#### Berichterstattung / Medienbeiträge

- Beitrag der UZHF im Fluntern Magazin (PDF, 163 KB) zum Projekt Bullinger Digital und dem bevorstehenden Citizen Science Workshop in der ZB.
- Netzwoche vom 24.3.2024 - Bullinger Briefe. Mit KI lassen sich vergangene Zeiten durchleuchten.
- SZRKG (Schweizerische Zeitschrift für Religions- und Kulturgeschichte) 117 (2023) – «Bullinger Digital»
- SZRKG (Schweizerische Zeitschrift für Religions- und Kulturgeschichte) 114 (2020) – «Bullinger Digital»
- Radio Life Channel – Briefe von Heinrich Bullinger werden digitalisiert
- UZH Foundation (Die Stiftung der UZH): Digitalisierung der Bullingerbriefe

