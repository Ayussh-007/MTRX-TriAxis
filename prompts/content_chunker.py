"""
MTRX-TriAxis | Prompt: Content Chunker (Module 2)
Splits structured curriculum text into atomic concept chunks.
"""

from langchain_core.prompts import ChatPromptTemplate

# System prompt for chunking structured content
CONTENT_CHUNKER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are preparing study material for an AI system.
Split the following content into meaningful chunks.

Rules:
* Each chunk should focus on ONE concept.
* Keep chunks between 100-300 words.
* Ensure each chunk is self-contained and understandable.
* Add a short title for each chunk.

Output format (valid JSON array):
[
  {{
    "title": "Concept Name",
    "content": "Explanation..."
  }}
]

IMPORTANT: Return ONLY the JSON array, no extra text before or after."""),
    ("human", "Content: {structured_text}")
])


def get_prompt():
    """Return the content chunker prompt template."""
    return CONTENT_CHUNKER_PROMPT
