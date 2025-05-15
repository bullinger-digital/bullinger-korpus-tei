# Dokumentation zur Spracherkennung im Bullinger-Korpus

## Sprachwechsel

Die 8500 manuell transkribierten Briefe liegen mit markierten Absätzen vor. Innerhalb der Absätze haben wir automatisch Satzgrenzen identifiziert und im XML markiert. In einem nachfolgenden Schritt haben wir automatisch die Sprache für jeden Satz bestimmt und als Attribut «lang» im XML markiert. Von insgesamt 222\'807 Sätzen haben wir 181\'115 Sätze als Latein markiert, 41\'483 als Frühneuhochdeutsch, 144 als Griechisch, 50 als Französisch, und 14 als Italienisch. Dazu haben wir einen eigenen Sprach-Erkenner trainiert, der insbesondere zwischen Latein und Frühneuhochdeutsch zuverlässig unterscheiden kann.

Da innerhalb von vielen Sätzen die Sprache wechselt, haben wir mit Hilfe eines eigens dafür entwickelten wortlisten-basierten Verfahrens ermittelt, wo Code-Switching vorliegt. Der Fokus lag dabei auf Folgen von mindestens zwei Wörtern, die von der Satzsprache abweichen. Also z.B. zwei oder mehr Wörter in Frühneuhochdeutsch, die in einem Satz auftreten, den wir als Latein markiert haben. Ein deutschsprachiger Satz mit Sprachwechsel nach Latein sieht also z.B. so aus:

Brief 9143.xml:

```xml
<s n="3" xml:lang="de">Dise summa, 120 gulden, ist mit etwas zusatz meiner gnädigen herren von armen und reichen <foreign xml:lang="la">in templis nostris</foreign> bey den thüren aufgehebt worden.</s>
```

In den 8500 manuell transkribierten Briefen haben wir 3345 Sätze mit Sprachwechsel markiert. Unser Verfahren zur Sprach-Erkennung und zur Markierung des Sprachwechsels haben wir beschrieben in:

    Volk, Martin; Fischer, Lukas; Scheurer, Patricia; Schwitter, Raphael; Ströbel, Phillip; Suter, Benjamin (2022): Nunc profana tractemus. Detecting Code-Switching in a Large Corpus of 16th Century Letters. In: Proceedings of LREC-2022, European Language Resources Association.

In einem ausführlicheren Artikel beschreiben wir die unterschiedlichen Arten des Sprachwechsels und schlagen eine Visualisierung für die zeitliche Entwicklung der Sprachverwendung zwischen bestimmten Korrespondenten vor.

    Volk, Martin; Fischer, Lukas; Scheurer, Patricia; Schwitter, Raphael; Ströbel, Phillip (2025): Code-Switching: Profiling and Classifying the Language Mix in a Large Corpus of 16th Century Letters. To be published in: Computational Approaches to Ancient Greek and Latin. De Gruyter.

### Griechisch

Nach Latein und Frühneuhochdeutsch ist Griechisch die dritthäufigste Sprache in den Bullinger-Briefen.

In den 3200 Briefen der HBBW-Edition und in den 5300 Briefen mit
manueller Transkription finden wir Griechisch in 1215 Sätzen (markiert mit lang="el"). Diese Zahl umfasst zwei Briefe, die vollständig in Griechisch geschrieben sind: 12945 und 12946, beide von Justus Vulteius an Heinrich Bullinger, 1547 oder 1548, mit 25 bzw. 47 Sätzen.

Wir haben die Griechisch-Passagen (also ganze Sätze oder auch Teilsätze und Einzelwörter) in den digitalen Briefen der HBBW-Edition manuell abgeglichen mit den gedruckten Entsprechungen in den Bänden 1 bis 21. Dabei haben wir auch die diakritischen Zeichen des Neu-Altgriechisch sorgfältig berücksichtigt.

Die Griechisch-Passagen in den 5300 Briefen mit manueller Transkription haben wir ebenfalls manuell kontrolliert und - wo nötig und aus dem Kontext zu erschliessen - korrigiert. In 86 Sätzen hat die transkribierende Person nur den Platzhalter "\[griechisch\]" eingetragen. Diese Stellen haben wir nicht aufgelöst. Wir überlassen diese Aufgabe einem zukünftigen Bearbeitungsschritt.

In den Briefen mit automatischer Transkription sind die Sprachen auf Satzebene nicht markiert.
