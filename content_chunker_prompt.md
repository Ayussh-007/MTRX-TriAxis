# Content Chunker Prompt
## MTRX-TriAxis | Module 2

---

## System Prompt

```
You are preparing study material for an AI system.
Split the following content into meaningful chunks.

Rules:
* Each chunk should focus on ONE concept.
* Keep chunks between 100–300 words.
* Ensure each chunk is self-contained and understandable.
* Add a short title for each chunk.

Output format:
[
  {
    "title": "Concept Name",
    "content": "Explanation..."
  }
]

Content: {structured_text}
```

---

## Usage Notes

- Feed the **output of Module 1 (Curriculum Analyzer)** as `{structured_text}` here.
- Each chunk in the output array is an atomic study unit — one concept, self-contained.
- The JSON array output plugs directly into Module 3 (downstream: quiz gen, flashcards, embeddings, etc.).
- Chunks between 100–300 words are optimally sized for RAG pipelines and LLM context windows.

---

## Pipeline Position

```
Raw Content
    ↓
[Module 1] Curriculum Analyzer   →  structured hierarchical text
    ↓
[Module 2] Content Chunker       →  JSON array of concept chunks
    ↓
[Module 3] ...
```

---

## Example Input

```
Topic: Mechanics
  Subtopic: Newton's Laws of Motion
    - Key points:
        • Objects remain at rest or in uniform motion unless acted on by an external force
        • Force equals mass times acceleration
    - Definitions:
        • Inertia: tendency of an object to resist changes in its state of motion
    - Important notes:
        • Formula: F = ma
        • First Law also known as the Law of Inertia
```

## Example Output

```json
[
  {
    "title": "Newton's First Law – Law of Inertia",
    "content": "Newton's First Law states that every object remains at rest or in uniform motion in a straight line unless acted upon by an external force. This property is called inertia — the tendency of an object to resist any change in its state of motion. For example, a book on a table stays still because no net force acts on it. This law applies to both stationary objects and objects moving at constant velocity."
  },
  {
    "title": "Newton's Second Law – F = ma",
    "content": "Newton's Second Law defines the relationship between force, mass, and acceleration. It states that the net force acting on an object equals the product of its mass and acceleration: F = ma. This means that a greater force produces greater acceleration, and a heavier object requires more force to achieve the same acceleration. The unit of force is the Newton (N), where 1 N = 1 kg·m/s²."
  }
]
```

---

*Created: 2026-04-15 | Project: MTRX-TriAxis*
