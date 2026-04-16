"""
MTRX-TriAxis | Prompt: Quiz Generator
Generates MCQ quizzes from curriculum content.
"""

from langchain_core.prompts import ChatPromptTemplate

QUIZ_GENERATOR_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are an expert quiz creator for students.
Given the following study material, generate {num_questions} multiple-choice questions.

Rules:
* Each question should test understanding, not just memorization.
* Provide exactly 4 options (A, B, C, D) for each question.
* Mark the correct answer clearly.
* Include a brief explanation for the correct answer.
* Questions should cover different aspects of the content.

Output format (valid JSON array):
[
  {{
    "question": "Question text here?",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct": "B",
    "explanation": "Brief explanation of why B is correct."
  }}
]

IMPORTANT: Return ONLY the JSON array, no extra text."""),
    ("human", """Topic: {topic}

Study Material:
{context}

Generate {num_questions} MCQ questions.""")
])


def get_prompt():
    """Return the quiz generator prompt template."""
    return QUIZ_GENERATOR_PROMPT
