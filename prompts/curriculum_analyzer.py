"""
MTRX-TriAxis | Prompt: Curriculum Analyzer (Module 1)
Cleans raw textbook/PDF content into a structured hierarchical format.
"""

from langchain_core.prompts import ChatPromptTemplate

# System prompt for structuring raw curriculum text
CURRICULUM_ANALYZER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert curriculum analyzer.
Given the following raw textbook or curriculum content, clean and structure it.

Instructions:
* Remove noise like page numbers, headers, footers.
* Identify main topics and subtopics.
* Preserve important definitions, formulas, and explanations.
* Format output in a clean hierarchical structure.

Output format:
Topic:
  Subtopic:
    - Key points
    - Definitions
    - Important notes"""),
    ("human", "Content: {input_text}")
])


def get_prompt():
    """Return the curriculum analyzer prompt template."""
    return CURRICULUM_ANALYZER_PROMPT
