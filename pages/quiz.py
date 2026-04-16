"""
MTRX-TriAxis | Quiz Page
Interactive quiz interface with MCQ generation, evaluation, and score tracking.
"""

import streamlit as st

from backend.quiz_engine import generate_quiz, evaluate_answers
from backend.student_model import list_students, record_quiz_score
from backend.rag_pipeline import vectorstore_exists, get_available_topics


st.markdown("# 📝 Quiz")
st.markdown("Generate and take quizzes based on your curriculum content.")
st.markdown("---")

# ----- Check Prerequisites -----
if not vectorstore_exists():
    st.warning("⚠️ No curriculum loaded. Please upload a PDF first.")
    st.page_link("pages/pdf_upload.py", label="Go to Upload Page", icon="📄")
    st.stop()

students = list_students()
if not students:
    st.warning("⚠️ No students registered. Please add a student first.")
    st.page_link("pages/student_view.py", label="Go to Student View", icon="🎒")
    st.stop()

# ----- Quiz Configuration -----
st.markdown("### ⚙️ Quiz Settings")

config_col1, config_col2, config_col3 = st.columns(3)

with config_col1:
    # Student selector
    student_options = {f"{s['name']}": s["id"] for s in students}
    selected_student = st.selectbox("Select Student:", options=list(student_options.keys()))
    student_id = student_options[selected_student]

with config_col2:
    # Topic input — try to get available topics
    available_topics = []
    try:
        available_topics = get_available_topics()
    except Exception:
        pass

    if available_topics:
        topic = st.selectbox("Select Topic:", options=available_topics)
    else:
        topic = st.text_input("Enter Topic:", placeholder="e.g., Newton's Laws of Motion")

with config_col3:
    num_questions = st.slider("Number of Questions:", min_value=3, max_value=10, value=5)

# ----- Generate Quiz -----
st.markdown("---")

if st.button("🎲 Generate Quiz", type="primary", use_container_width=True):
    if not topic:
        st.warning("Please enter or select a topic.")
    else:
        with st.spinner(f"Generating {num_questions} questions on '{topic}'..."):
            quiz = generate_quiz(topic, num_questions)

        if quiz.get("error"):
            st.error(quiz["error"])
        elif quiz["questions"]:
            st.session_state["current_quiz"] = quiz
            st.session_state["quiz_student_id"] = student_id
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_answers"] = {}
            st.success(f"✅ Generated {len(quiz['questions'])} questions!")
            st.rerun()
        else:
            st.error("Failed to generate quiz. Try a different topic.")

# ----- Display Quiz -----
if "current_quiz" in st.session_state and not st.session_state.get("quiz_submitted", False):
    quiz = st.session_state["current_quiz"]

    st.markdown(f"### 📋 Quiz: {quiz['topic']}")
    st.caption(f"Quiz ID: {quiz['quiz_id']} | Questions: {len(quiz['questions'])}")
    st.markdown("---")

    # Render each question
    for i, q in enumerate(quiz["questions"]):
        st.markdown(
            f"""
            <div style='background: #1a1d29; border-radius: 10px; padding: 1.2rem;
                        margin-bottom: 1rem; border: 1px solid #333;'>
                <strong style='color: #6C63FF;'>Q{i + 1}.</strong> {q['question']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Radio buttons for options
        options = q.get("options", {})
        option_labels = [f"{key}: {val}" for key, val in options.items()]

        selected = st.radio(
            f"Select your answer for Q{i + 1}:",
            options=list(options.keys()),
            format_func=lambda x, opts=options: f"{x}: {opts.get(x, '')}",
            key=f"q_{i}",
            label_visibility="collapsed",
        )

        st.session_state["quiz_answers"][i] = selected
        st.markdown("")

    # Submit button
    st.markdown("---")
    if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
        st.session_state["quiz_submitted"] = True
        st.rerun()

# ----- Quiz Results -----
if st.session_state.get("quiz_submitted", False) and "current_quiz" in st.session_state:
    quiz = st.session_state["current_quiz"]
    answers = st.session_state.get("quiz_answers", {})

    # Evaluate
    evaluation = evaluate_answers(quiz, answers)

    # Record score in database
    student_id = st.session_state.get("quiz_student_id")
    if student_id:
        record_quiz_score(
            student_id=student_id,
            quiz_id=quiz["quiz_id"],
            topic=quiz["topic"],
            score=evaluation["score"],
            max_score=evaluation["max_score"],
        )

    # Display results
    st.markdown("### 📊 Quiz Results")

    # Score summary
    score = evaluation["score"]
    max_score = evaluation["max_score"]
    percentage = evaluation["percentage"]

    # Score color
    if percentage >= 70:
        score_color = "#4CAF50"
        emoji = "🎉"
        message = "Excellent work!"
    elif percentage >= 50:
        score_color = "#FF9800"
        emoji = "👍"
        message = "Good effort! Keep practicing."
    else:
        score_color = "#F44336"
        emoji = "💪"
        message = "Don't give up! Review the topics and try again."

    st.markdown(
        f"""
        <div style='text-align: center; background: #1a1d29; border-radius: 12px;
                    padding: 2rem; border: 2px solid {score_color}; margin-bottom: 1.5rem;'>
            <span style='font-size: 3rem;'>{emoji}</span>
            <h2 style='color: {score_color}; margin: 0.5rem 0;'>
                {score} / {max_score} ({percentage}%)
            </h2>
            <p style='color: #aaa;'>{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Per-question results
    st.markdown("### 📝 Question Review")

    for result in evaluation["results"]:
        idx = result["question_index"]
        is_correct = result["is_correct"]

        icon = "✅" if is_correct else "❌"
        border_color = "#4CAF50" if is_correct else "#F44336"

        with st.expander(f"{icon} Q{idx + 1}: {result['question'][:80]}...", expanded=not is_correct):
            st.markdown(f"**Your answer:** {result['student_answer']}")
            st.markdown(f"**Correct answer:** {result['correct_answer']}")
            if result.get("explanation"):
                st.info(f"💡 **Explanation:** {result['explanation']}")

    # New quiz button
    st.markdown("---")
    if st.button("🔄 Take Another Quiz", use_container_width=True):
        for key in ["current_quiz", "quiz_submitted", "quiz_answers", "quiz_student_id"]:
            st.session_state.pop(key, None)
        st.rerun()
