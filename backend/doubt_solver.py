"""
MTRX-TriAxis | Stage 4: Doubt Solver
Answers student questions using the RAG pipeline for curriculum-grounded responses.
"""

from backend.rag_pipeline import rag_query, vectorstore_exists


def answer_doubt(question: str) -> dict:
    """
    Answer a student's doubt using the RAG pipeline.

    Retrieves relevant curriculum content and uses the LLM to generate
    a clear, student-friendly explanation.

    Args:
        question: The student's question/doubt as a string.

    Returns:
        Dict with:
            - answer: The generated explanation.
            - sources: List of source topic titles used.
            - error: Error message if something went wrong, else None.
    """
    if not question or not question.strip():
        return {
            "answer": "",
            "sources": [],
            "error": "Please enter a question.",
        }

    if not vectorstore_exists():
        return {
            "answer": "",
            "sources": [],
            "error": "No curriculum loaded. Please upload and process a PDF first.",
        }

    try:
        result = rag_query(question)
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "error": None,
        }
    except Exception as e:
        return {
            "answer": "",
            "sources": [],
            "error": f"Error answering doubt: {str(e)}",
        }
