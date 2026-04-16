"""
MTRX-TriAxis | Feature 5: Class Weakness Detection + Auto Doubt Sheet
Aggregates class-wide weak topics and generates a printable doubt-resolution sheet.
"""

from backend.llm_utils import get_llm
from backend.student_model import (
    list_students, get_weak_topics, get_class_topic_averages,
)
from backend.rag_pipeline import retrieve_context, vectorstore_exists


def get_top_weak_topics(top_n: int = 3) -> list[dict]:
    """
    Identify the top N weakest topics across the entire class.

    Aggregates weak topics from all students and ranks by frequency
    and severity.

    Args:
        top_n: Number of top weak topics to return.

    Returns:
        List of dicts: [{topic, frequency, class_avg, severity}, ...]
    """
    students = list_students()
    topic_freq = {}  # topic → count of students who have it as weak
    class_avgs = get_class_topic_averages()

    # Count how many students find each topic weak
    for student in students:
        weak = get_weak_topics(student["id"])
        for topic in weak:
            topic_freq[topic] = topic_freq.get(topic, 0) + 1

    # Build ranked list
    result = []
    for topic, freq in topic_freq.items():
        avg = class_avgs.get(topic, {}).get("average", 0)

        # Severity score: higher = more severe (combines frequency + low scores)
        severity = freq * (100 - avg) / 100

        result.append({
            "topic": topic,
            "frequency": freq,
            "students_struggling": freq,
            "total_students": len(students),
            "class_avg": avg,
            "severity": round(severity, 1),
        })

    # Sort by severity descending
    result.sort(key=lambda x: x["severity"], reverse=True)
    return result[:top_n]


def generate_doubt_sheet(topics: list[str] = None) -> str:
    """
    Auto-generate a doubt-resolution sheet for the class's weakest topics.

    For each weak topic:
        - Retrieves relevant curriculum content (RAG)
        - Generates common doubts and clear explanations
        - Formats as a printable study sheet

    Args:
        topics: List of topic names. If None, uses top 3 weak topics.

    Returns:
        Markdown-formatted doubt sheet ready for distribution.
    """
    # Get top weak topics if not specified
    if topics is None:
        weak = get_top_weak_topics(top_n=3)
        topics = [w["topic"] for w in weak]

    if not topics:
        return "No weak topics identified. Students are performing well!"

    # Retrieve context for each topic (if vectorstore exists)
    topic_contexts = {}
    if vectorstore_exists():
        for topic in topics:
            docs = retrieve_context(topic, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            topic_contexts[topic] = context

    # Build the prompt
    topics_section = ""
    for topic in topics:
        ctx = topic_contexts.get(topic, "No specific curriculum content available.")
        topics_section += f"\n### Topic: {topic}\nCurriculum Context:\n{ctx}\n"

    prompt = f"""You are an expert teacher creating a study aid for struggling students.

Generate a "Doubt Resolution Sheet" for the following weak topics.
For each topic, provide:

1. **Key Concepts Summary** — Concise review of the core concepts
2. **Common Doubts** — 3-4 questions students typically struggle with
3. **Clear Explanations** — Simple, step-by-step answers to each doubt
4. **Quick Practice** — 2 simple practice questions with answers

Format the output as a clean, printable study sheet:

# 📝 Doubt Resolution Sheet
---
{topics_section}

Make explanations beginner-friendly.
Use analogies and real-world examples where possible.
Keep each topic section concise but thorough."""

    llm = get_llm(temperature=0.6)
    return llm.invoke(prompt)
