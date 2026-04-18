"""
MTRX-TriAxis | Student Portal
Personal dashboard for authenticated students — shows assigned content,
quiz scores, learning paths, doubt solving, and AI feedback.
"""

import streamlit as st
from datetime import date

from backend.auth import get_logged_in_student, logout_student, is_student_logged_in
from backend.student_model import (
    get_overall_score, get_attendance_rate, get_topic_scores,
    get_weak_topics, get_strong_topics, generate_learning_path,
)
from backend.attendance_intelligence import (
    get_performance_trend, generate_performance_feedback,
)
from backend.content_sharing import get_student_assignments, get_shared_content, mark_content_accessed
from backend.doubt_solver import answer_doubt
from backend.rag_pipeline import vectorstore_exists, get_available_topics


# ----- Auth Guard -----
if not is_student_logged_in():
    st.warning("🔒 Please login to access your portal.")
    st.page_link("pages/student_login.py", label="Go to Login →", icon="🔐")
    st.stop()

student = get_logged_in_student()
student_id = student["id"]

# ----- Header -----
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown(f"# 🎒 Welcome, {student['name']}!")
    st.caption(f"Student ID: {student.get('login_id', 'N/A')} | Logged in")

with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        logout_student()
        st.switch_page("pages/student_login.py")

st.markdown("---")

# ----- Key Metrics -----
overall = get_overall_score(student_id)
attendance = get_attendance_rate(student_id)
weak = get_weak_topics(student_id)
strong = get_strong_topics(student_id)
topic_scores = get_topic_scores(student_id)
trend = get_performance_trend(student_id)

trend_icon = {"improving": "📈", "declining": "📉", "stable": "📊",
              "insufficient_data": "❓"}.get(trend["overall_trend"], "📊")

m1, m2, m3, m4 = st.columns(4)
m1.metric("📈 Overall Score", f"{overall}%")
m2.metric("📅 Attendance", f"{attendance}%")
m3.metric("⚠️ Weak Topics", len(weak))
m4.metric(f"{trend_icon} Trend", trend["overall_trend"].title())

# ----- Tabs for different sections -----
tab_progress, tab_assignments, tab_doubts, tab_path = st.tabs([
    "📊 My Progress", "📋 Assignments", "💬 Ask Doubts", "🎯 Learning Path"
])

# ===== TAB 1: Progress Tracking (Feature 7) =====
with tab_progress:
    st.markdown("### 📊 My Performance")

    if topic_scores:
        for topic, score in sorted(topic_scores.items(), key=lambda x: x[1]):
            if score >= 70:
                color = "#4CAF50"
                icon = "✅"
            elif score >= 50:
                color = "#FF9800"
                icon = "⚠️"
            else:
                color = "#F44336"
                icon = "❌"

            st.markdown(
                f"""
                <div style='background: #1a1d29; padding: 0.8rem 1rem; border-radius: 8px;
                            margin-bottom: 0.5rem; border-left: 4px solid {color};
                            display: flex; justify-content: space-between; align-items: center;'>
                    <span>{icon} {topic}</span>
                    <span style='color: {color}; font-weight: bold;'>{score}%</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No quiz scores yet. Take a quiz to see your performance!")

    # Performance Evolution
    if trend["overall_trend"] != "insufficient_data":
        st.markdown("---")
        st.markdown("### 📈 Performance Evolution")
        st.markdown(trend["summary"])

        if trend["topic_trends"]:
            for topic, data in trend["topic_trends"].items():
                if data["trend"] == "improving":
                    t_color = "#4CAF50"
                    t_icon = "📈"
                elif data["trend"] == "declining":
                    t_color = "#F44336"
                    t_icon = "📉"
                else:
                    t_color = "#FF9800"
                    t_icon = "📊"

                st.markdown(
                    f"""
                    <div style='background: #1a1d29; padding: 0.6rem 1rem; border-radius: 8px;
                                margin-bottom: 0.4rem; border-left: 3px solid {t_color};
                                display: flex; justify-content: space-between;'>
                        <span>{t_icon} {topic}</span>
                        <span style='color: {t_color};'>
                            {data['early_avg']}% → {data['recent_avg']}%
                            ({data['change']:+}%)
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # AI Performance Feedback
    st.markdown("---")
    if st.button("🧠 Get AI Performance Feedback", key="portal_perf_btn", type="primary"):
        with st.spinner("Analyzing your performance..."):
            feedback = generate_performance_feedback(student_id)
            st.session_state[f"portal_feedback_{student_id}"] = feedback

    if f"portal_feedback_{student_id}" in st.session_state:
        st.markdown(st.session_state[f"portal_feedback_{student_id}"])


# ===== TAB 2: Assigned Content =====
with tab_assignments:
    st.markdown("### 📋 Assigned Content")

    assignments = get_student_assignments(student_id)

    if not assignments:
        st.info("No content assigned yet. Your teacher will share materials with you.")
    else:
        for a in assignments:
            accessed_badge = "✅ Viewed" if a["accessed"] else "🆕 New"
            type_emoji = {"quiz": "📝", "learning_path": "🎯", "doubt_sheet": "📋"}.get(
                a["content_type"], "📄"
            )

            with st.expander(f"{type_emoji} {a['content_type'].replace('_', ' ').title()} — {accessed_badge}"):
                content = get_shared_content(a["share_id"])
                if content:
                    # Mark as accessed
                    if not a["accessed"]:
                        mark_content_accessed(a["share_id"], student_id)

                    data = content["content_data"]

                    if content["content_type"] == "quiz":
                        st.markdown(f"**Topic:** {data.get('topic', 'Unknown')}")
                        st.markdown(f"**Questions:** {len(data.get('questions', []))}")
                        st.caption("Take this quiz in the Quiz page.")

                    elif content["content_type"] == "doubt_sheet":
                        st.markdown(data.get("content", "No content available."))

                    elif content["content_type"] == "learning_path":
                        st.markdown(data.get("content", "No content available."))

                    else:
                        st.json(data)


# ===== TAB 3: Doubt Solving =====
with tab_doubts:
    st.markdown("### 💬 Ask a Doubt")

    if not vectorstore_exists():
        st.warning("No curriculum loaded yet. Ask your teacher to upload study material.")
    else:
        doubt_question = st.text_area(
            "Type your question here:",
            placeholder="e.g., What is Newton's Second Law and how is it applied?",
            height=100,
            key="portal_doubt_input",
        )

        if st.button("🔍 Get Answer", type="primary", key="portal_doubt_btn"):
            if doubt_question.strip():
                with st.spinner("Searching curriculum and generating answer..."):
                    result = answer_doubt(doubt_question)

                if result.get("error"):
                    st.error(result["error"])
                else:
                    st.markdown("#### 📖 Answer")
                    st.markdown(result["answer"])

                    if result.get("sources"):
                        st.markdown("---")
                        st.caption("**Sources:** " + ", ".join(result["sources"]))
            else:
                st.warning("Please enter a question.")


# ===== TAB 4: Learning Path =====
with tab_path:
    st.markdown("### 🎯 My Learning Path")

    if st.button("🧠 Generate Personalized Learning Path", type="primary",
                 use_container_width=True, key="portal_path_btn"):
        with st.spinner("Analyzing your performance and building a study plan..."):
            available = []
            if vectorstore_exists():
                try:
                    available = get_available_topics()
                except Exception:
                    pass

            path = generate_learning_path(student_id, available)
            st.session_state[f"portal_path_{student_id}"] = path

    if f"portal_path_{student_id}" in st.session_state:
        st.markdown(st.session_state[f"portal_path_{student_id}"])
