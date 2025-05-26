# Projektdokumentation: Verschlagwortung im Briefwechsels von Heinrich Bullinger

## Zielsetzung

Ziel dieses Projekts war die automatische Identifikation zentraler Themen im historischen Briefwechsel von Heinrich Bullinger. Aufgrund der Komplexität der Texte war ein hybrides Verfahren notwendig, das manuelle Annotation, Prompt Engineering und grosse Sprachmodelle (LLMs)
kombiniert.

Diese Aufgabe ist besonders herausfordernd aus folgenden Gründen:

1.  Es gibt keine Verschlagwortung in der gedruckten Edition -- somit fehlt Trainingsmaterial für überwachte Klassifikation.

2.  Standard-NLP-Werkzeuge (z. B. Lemmatisierer) versagen häufig bei historischen Texten, sogar bei Latein und insbesondere bei Frühneuhochdeutsch.

3.  Die Sprache der humanistischen Korrespondenz ist metaphorisch, die Themen sind oft implizit und nicht direkt benannt.

4.  Zentrale Entitäten erscheinen in unterschiedlichen Formen (z. B. „Schwytzern", „Helvetici", „aidgnossen", „Elvetiis" -- alle bezeichnen die Schweizer), was automatisches Linking und Grounding erschwert.

5.  Obwohl grosse Sprachmodelle historische Texte verstehen können, weisen sie einzelnen Briefen inkonsistente und schwer nachvollziehbare Themen zu.

---

## Methodik

### *Schritt 1: Definition thematischer Kategorien*

In Zusammenarbeit mit einer historischen Expertin haben wir 11 klar definierte, historisch relevante Themen festgelegt. Jedes Thema wurde mit einer kurzen, präzisen Beschreibung versehen, um sowohl für Menschen als auch für KI eindeutig interpretierbar zu sein. Die Liste wurde iterativ anhand von Annotationstests und Modellfeedback weiterentwickelt. 🔗 [Themen](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/blob/main/Verschlagwortung/topics/topics4_en.json)

### *Schritt 2: Menschliche Annotation*

Drei Forschende annotierten eine repräsentative Auswahl von 17 Briefen 🔗 [Testdateien](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/test_files) anhand der vordefinierten Themen.Das Annotationsschema war wie folgt:

- `0` — Thema ist **nicht vorhanden**
- `1` — Thema ist **klar zentral**
- `2` — Thema ist **vorhanden, aber die Zentralität ist unklar**

Um voneinander abweichende Annotationen zu konsolidieren, entwickelten wir ein **regelbasiertes Fusionsschema** (siehe unten). Diese Annotationen flossen auch in die Verfeinerung der Themenliste und der KI-Prompts ein. 🔗 [Menschliche Annotationen](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/annotations/humans)

#### Fusion der Annotationen und finale Labels

Im Folgenden sind Beispiele für Annotationskombinationen und das daraus resultierende **finale Label** aufgeführt:

**Finales Label: 0**
- `0x3` — Alle drei Annotator:innen vergaben `0`
- `1x1, 0x1, 2x1` — Jeweils eine Vergabe von `1`, `0` und `2`
- `2x2, 0x1` — Zwei Vergaben von `2`, eine von `0`
- `0x2, 1x1`
- `0x2, 2x1`

**Finales Label: 1**
- `1x2, 2x1`
- `1x2, 0x1`

**Finales Label: 2**
- `1x1, 2x2`
- `2x3`

### *Schritt 3: Annotation mit Sprachmodellen (LLMs)*

Wir entwickelten maßgeschneiderte Prompts, die die KI anweisen, pro Brief nur 2–3 wirklich zentrale Themen aus der von Experten definierten Themenliste auszuwählen. Wir befragten zwei große Sprachmodelle: GPT-4o und Deepseek mit folgendem Persona-System-Prompt:

```plaintext
You are a historian working with the correspondence of Heinrich Bullinger (1504-1575). You have a list of topics here: {topics_data}. You identify these topics for each letter in the correspondence.
```

Jedes Modell erhielt die Themenbeschreibungen und wurde beauftragt, jeden Brief entsprechend zu annotieren. Die Prompts sind hier zu finden: 🔗  [Prompts](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/prompts). Der finale Prompt lautete:

```plaintext
Letter content: {{content}}
Assign two or three topics (if the letter is long) from the list of topics to the letter. Select only topics that are truly central to the letter's content. Do not assign topics based on brief mentions, focus only on the main themes conveyed by the author. If topics overlap, choose the most central one rather than assigning multiple similar topics.
Provide the result as a JSON object like this: 
{
    "predefined_topics": [
        "topic1", "topic2"
        ]
}
```
Wir zeichneten auf, wie oft (von 10 Antworten) jedes Thema pro Brief zugewiesen wurde. Um Unterschiede zwischen den Modellen auszugleichen, verwendeten wir eine Mischstrategie:

- Dominante Themen (z. B. „Anfragen und Bitten", „Militärische und politische Angelegenheiten") wurden nur übernommen, wenn beide Modelle sie mit mindestens 90 % Sicherheit zuordneten.

- Alle anderen Themen wurden berücksichtigt, wenn ein Modell mindestens 60 % erreichte und das andere mindestens 20 %.

### *Schritt 4: Evaluation*

Eine qualitative Stichprobe bestätigte, dass die finalen Annotationen kohärent und sinnvoll sind. Es ist uns bewusst, dass einige Grenzfälle weiterhin bestehen und einer fachlichen Diskussion bedürfen.
