# Project Documentation: Thematic Annotation of Bullinger's Correspondence

## Objective

The aim of this project is the automatic identification of central themes in the historical correspondence of Heinrich Bullinger. Due to the complex nature of the texts, the task required a hybrid method combining human annotation, prompt engineering, and large language models (LLMs).

This task is particularly challenging due to the following challenges:

1.  The absence of thematic indexing in the printed edition means there is no training data for supervised classification.

2.  The Standard NLP tools (e.g., lemmatizers) often fail on historical texts, especially in Latin and Early New High German.

3.  The language of humanist correspondence is metaphorical and nuanced, with themes frequently implied rather than stated directly.

4.  The key entities appear in diverse forms (e.g., "Schwytzern", "Helvetici", "aidgnossen", "Elvetiis" -- all referring to the Swiss), complicating automatic linking and grounding.

5.  While large language models can interpret historical texts, they assign inconsistent and opaque theme sets across the correspondance.

---
## Methodology

### *Step 1. Definition of Thematic Categories*

In collaboration with a historical expert, we defined 11 clear, historically grounded themes. Each theme has a short, precise description to guide both human and AI annotations. This list was refined iteratively based on annotation trials and model feedback. 🔗 [Topics](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/blob/main/Verschlagwortung/topics/topics4_en.json)

### *Step 2. Human Annotation*

Three researchers annotated a representative set of 17 letters 🔗 [Test files](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/test_files) using the predefined topics.  
The annotation scheme was as follows:

- `0` — Topic is **not present**
- `1` — Topic is **clearly central**
- `2` — Topic is **present, but centrality is unclear**

To consolidate diverging annotations, we established a **rule-based fusion scheme** (see below). These annotations also informed refinement of the topics and AI prompts. 🔗 [Human Annotations](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/annotations/humans)

#### Annotation Fusion and Final Labels

Below are examples of annotation combinations and their resulting **final label**:

**Final Label: 0**
- `0x3` — All three annotators assigned `0`
- `1x1, 0x1, 2x1` — One each assigned `1`, `0`, and `2`
- `2x2, 0x1` — Two assigned `2`, one assigned `0`
- `0x2, 1x1`
- `0x2, 2x1`

**Final Label: 1**
- `1x2, 2x1`
- `1x2, 0x1`

**Final Label: 2**
- `1x1, 2x2`
- `2x3`

### *Step 3. Annotation with LLMs* 

We designed tailored prompts instructing the AI to select only 2--3 truly central themes per letter based on the expert-defined topic list. We queried two large language models: GPT-4o and Deepseek using the following persona system prompt: 

``` text
You are a historian working with the correspondence of Heinrich Bullinger (1504-1575). You have a list of topics here: {topics_data}. You identify these topics for each letter in the correspondence.
```

Each model was provided with the topic descriptions and tasked with annotating each letter accordingly. The prompts can be found here: 🔗 [Prompts](https://github.com/bullinger-digital/bullinger-auxiliary-scripts/tree/main/Verschlagwortung/prompts). The final prompt was:

```text
Letter content: {{content}}
Assign two or three topics (if the letter is long) from the list of topics to the letter. Select only topics that are truly central to the letter's content. Do not assign topics based on brief mentions, focus only on the main themes conveyed by the author. If topics overlap, choose the most central one rather than assigning multiple similar topics.
Provide the result as a JSON object like this: 
{
    "predefined_topics": [
        "topic1", "topic2"
        ]
}
```

We recorded how often (out of 10 responses) each theme was assigned per letter. To reconcile differences between models, we used a mixed strategy:

- Dominant topics (e.g., "Requests and Petitions", "Military and Political Affairs") were included only if both models assigned them with ≥ 90% certainty.

- All other topics were included if one model reached ≥ 60% and the other ≥ 20%.

### *Step 4. Evaluation*

A qualitative review confirmed that the final annotations are coherent and meaningful. We acknowledge that edge cases remain and may require further expert discussion.
