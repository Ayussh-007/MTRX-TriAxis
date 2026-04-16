"""
MTRX-TriAxis | Feature 6: Multi-Step AI Reasoning Agent
Simulates an AI agent workflow that chains multiple analysis steps
to produce comprehensive, context-aware recommendations.

Pipeline:
    1. Analyze student data
    2. Retrieve relevant curriculum (RAG)
    3. Identify weak areas
    4. Generate: learning plan + quiz + suggestions
"""

import json
from backend.llm_utils import get_llm
from backend.student_model import (
    get_student, get_overall_score, get_attendance_rate,
    get_weak_topics, get_strong_topics, get_topic_scores,
    get_student_scores,
)
from backend.attendance_intelligence import (
    get_attendance_status, get_performance_trend,
)
from backend.teacher_feedback import build_style_context
from backend.rag_pipeline import retrieve_context, vectorstore_exists
from backend.quiz_engine import generate_quiz
from backend.weather_context import get_weather, get_context_suggestion


def run_agent_pipeline(student_id: int, city: str = None) -> dict:
    """
    Run the full multi-step AI reasoning pipeline for a student.

    This simulates an AI agent that performs sequential analysis steps,
    each building on the previous step's output.

    Steps:
        1. ANALYZE  — Gather and analyze all student data
        2. RETRIEVE — Fetch relevant curriculum for weak topics (RAG)
        3. IDENTIFY — Detect patterns, risks, and opportunities
        4. GENERATE — Produce learning plan, quiz suggestion, and advice

    Args:
        student_id: The student to analyze.
        city: Optional city for weather context.

    Returns:
        Dict with step-by-step reasoning and final outputs.
    """
    student = get_student(student_id)
    if not student:
        return {"error": "Student not found", "steps": []}

    steps = []
    context = {}

    # ============================================================
    # STEP 1: ANALYZE — Gather all student data
    # ============================================================
    step1 = {"name": "📊 Analyze Student Data", "status": "running"}

    overall = get_overall_score(student_id)
    attendance_status = get_attendance_status(student_id)
    weak = get_weak_topics(student_id)
    strong = get_strong_topics(student_id)
    topic_scores = get_topic_scores(student_id)
    trend = get_performance_trend(student_id)
    recent = get_student_scores(student_id)[:5]

    context["student"] = student
    context["overall_score"] = overall
    context["attendance"] = attendance_status
    context["weak_topics"] = weak
    context["strong_topics"] = strong
    context["topic_scores"] = topic_scores
    context["trend"] = trend
    context["recent_scores"] = recent

    step1["status"] = "complete"
    step1["findings"] = {
        "overall_score": f"{overall}%",
        "attendance_rate": f"{attendance_status['attendance_rate']}%",
        "attendance_risk": attendance_status["risk_level"],
        "weak_topics": weak[:5],
        "strong_topics": strong[:3],
        "performance_trend": trend["overall_trend"],
    }
    steps.append(step1)

    # ============================================================
    # STEP 2: RETRIEVE — Fetch curriculum context for weak topics
    # ============================================================
    step2 = {"name": "🔍 Retrieve Curriculum Context", "status": "running"}

    curriculum_context = ""
    if vectorstore_exists() and weak:
        # Retrieve context for up to 3 weakest topics
        for topic in weak[:3]:
            docs = retrieve_context(topic, k=2)
            for doc in docs:
                curriculum_context += f"\n[{doc.metadata.get('title', topic)}]\n{doc.page_content}\n"

    context["curriculum"] = curriculum_context

    step2["status"] = "complete"
    step2["findings"] = {
        "topics_searched": weak[:3],
        "context_retrieved": bool(curriculum_context),
        "context_length": len(curriculum_context),
    }
    steps.append(step2)

    # ============================================================
    # STEP 3: IDENTIFY — Detect patterns and risks
    # ============================================================
    step3 = {"name": "🧠 Identify Patterns & Risks", "status": "running"}

    risks = []
    opportunities = []

    # Attendance risk
    if attendance_status["risk_level"] in ["high", "critical"]:
        risks.append(f"Low attendance ({attendance_status['attendance_rate']}%) — student is missing content")
    if attendance_status["absence_streak"] >= 3:
        risks.append(f"Absent {attendance_status['absence_streak']} consecutive days")

    # Performance risk
    if trend["overall_trend"] == "declining":
        risks.append(f"Performance declining ({trend['overall_change']:+}%)")
    if overall < 40:
        risks.append(f"Overall score critically low ({overall}%)")

    # Topic-specific risks
    for topic in weak[:3]:
        score = topic_scores.get(topic, 0)
        risks.append(f"Struggling with '{topic}' (avg: {score}%)")

    # Opportunities
    if trend["overall_trend"] == "improving":
        opportunities.append(f"Performance improving ({trend['overall_change']:+}%)")
    for topic in strong[:2]:
        opportunities.append(f"Strong in '{topic}'")

    # Teacher style context
    style_context = build_style_context()

    # Weather context
    weather_note = ""
    if city:
        weather = get_weather(city)
        if weather:
            weather_note = get_context_suggestion(weather)

    context["risks"] = risks
    context["opportunities"] = opportunities
    context["style_context"] = style_context
    context["weather_note"] = weather_note

    step3["status"] = "complete"
    step3["findings"] = {
        "risks_detected": len(risks),
        "risks": risks,
        "opportunities": opportunities,
        "teacher_style_applied": bool(style_context),
        "weather_context": weather_note[:100] if weather_note else "N/A",
    }
    steps.append(step3)

    # ============================================================
    # STEP 4: GENERATE — Produce comprehensive recommendations
    # ============================================================
    step4 = {"name": "✨ Generate Recommendations", "status": "running"}

    # Build the master prompt with all gathered context
    prompt = f"""You are an advanced AI educational advisor performing multi-step reasoning.

You have analyzed a student and gathered the following data through sequential analysis steps:

## Step 1: Student Profile
- Name: {student['name']}
- Overall Score: {overall}%
- Attendance: {attendance_status['attendance_rate']}% ({attendance_status['status']})
- Performance Trend: {trend['overall_trend']} ({trend['overall_change']:+}%)
- Weak Topics: {', '.join(weak) if weak else 'None'}
- Strong Topics: {', '.join(strong) if strong else 'None'}

## Step 2: Relevant Curriculum
{curriculum_context[:1500] if curriculum_context else 'No curriculum context available.'}

## Step 3: Identified Risks & Opportunities
Risks:
{chr(10).join('- ' + r for r in risks) if risks else '- No major risks identified'}

Opportunities:
{chr(10).join('- ' + o for o in opportunities) if opportunities else '- No specific opportunities identified'}

## Teacher Style Preferences
{style_context}

## Weather Context
{weather_note if weather_note else 'No weather data available.'}

---

Based on this multi-step analysis, generate:

### 📋 Comprehensive Student Report

#### 1. Situation Summary
(2-3 sentence overview of where this student stands)

#### 2. Personalized Learning Plan
(Specific weekly plan addressing their weak topics.
If teacher prefers visual style → suggest diagrams/videos.
If class is slow → simplify the plan.
If attendance is low → include catch-up elements.)

#### 3. Recommended Quiz Topics
(Top 3 topics to quiz on next, with reasoning)

#### 4. Immediate Actions
(3 specific things the student should do THIS WEEK)

#### 5. Teacher Advisory
(What the teacher should know/do for this student)

Be concise, actionable, and encouraging."""

    llm = get_llm(temperature=0.7)
    recommendation = llm.invoke(prompt)

    step4["status"] = "complete"
    step4["output"] = recommendation
    steps.append(step4)

    return {
        "student_name": student["name"],
        "steps": steps,
        "final_recommendation": recommendation,
        "metadata": {
            "risks_count": len(risks),
            "weak_topics_count": len(weak),
            "trend": trend["overall_trend"],
            "attendance_risk": attendance_status["risk_level"],
        }
    }
