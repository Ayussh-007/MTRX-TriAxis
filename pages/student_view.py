"""
MTRX-TriAxis | Student View Page
Student profile, attendance intelligence, performance evolution,
learning paths, and doubt-solving.
"""

import streamlit as st
from datetime import date

from backend.student_model import (
    list_students, add_student, get_student,
    get_overall_score, get_attendance_rate, get_topic_scores,
    get_weak_topics, get_strong_topics, record_attendance,
    generate_learning_path,
)
from backend.attendance_intelligence import (
    get_attendance_status, get_attendance_history,
    generate_recovery_plan, get_performance_trend,
    generate_performance_feedback,
)
from backend.doubt_solver import answer_doubt
from backend.rag_pipeline import vectorstore_exists, get_available_topics


st.markdown("# 🎒 Student View")
st.markdown("---")

# ----- Student Management Section -----
col_mgmt1, col_mgmt2 = st.columns([1, 2])

with col_mgmt1:
    st.markdown("### ➕ Add Student")
    with st.form("add_student_form", clear_on_submit=True):
        new_name = st.text_input("Name", placeholder="e.g., Ayush Sharma")
        new_email = st.text_input("Email (optional)", placeholder="ayush@example.com")
        new_login_id = st.text_input("Login ID", placeholder="e.g., STU001",
                                     help="Unique ID for student self-service login.")
        submitted = st.form_submit_button("Add Student", type="primary")

        if submitted and new_name.strip():
            try:
                sid = add_student(new_name.strip(), new_email.strip() or None,
                                  new_login_id.strip() or None)
                st.success(f"✅ Added {new_name} (ID: {sid})")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col_mgmt2:
    st.markdown("### 👥 Select Student")
    students = list_students()

    if not students:
        st.info("No students registered yet. Add a student to get started.")
        st.stop()

    # Student selector
    student_options = {f"{s['name']} (ID: {s['id']})": s["id"] for s in students}
    selected_label = st.selectbox("Choose a student:", options=list(student_options.keys()))
    selected_id = student_options[selected_label]
    student = get_student(selected_id)

st.markdown("---")

# ----- Student Dashboard -----
if student:
    st.markdown(f"## 📊 Dashboard: {student['name']}")

    # Key metrics
    overall = get_overall_score(selected_id)
    attendance = get_attendance_rate(selected_id)
    weak = get_weak_topics(selected_id)
    strong = get_strong_topics(selected_id)
    topic_scores = get_topic_scores(selected_id)

    # Feature 2: Attendance status with risk detection
    att_status = get_attendance_status(selected_id)

    # Feature 4: Performance trend
    trend = get_performance_trend(selected_id)
    trend_icon = {"improving": "📈", "declining": "📉", "stable": "📊",
                  "insufficient_data": "❓"}.get(trend["overall_trend"], "📊")

    # Metric cards (expanded with trends)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("📈 Overall Score", f"{overall}%")
    m2.metric(
        f"{att_status['status_emoji']} Attendance",
        f"{attendance}%",
        delta=f"Streak: {att_status['absence_streak']}d absent" if att_status['absence_streak'] > 0 else None,
        delta_color="inverse",
    )
    m3.metric("⚠️ Weak Topics", len(weak))
    m4.metric("✅ Strong Topics", len(strong))
    m5.metric(
        f"{trend_icon} Trend",
        trend["overall_trend"].title(),
        delta=f"{trend['overall_change']:+}%" if trend["overall_trend"] != "insufficient_data" else None,
        delta_color="normal" if trend["overall_change"] >= 0 else "inverse",
    )

    # ----- Feature 2: Attendance Intelligence Alert -----
    if att_status["risk_level"] in ["high", "critical"]:
        st.markdown("---")
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #4a0000, #1a1d29);
                        border-radius: 10px; padding: 1rem 1.2rem;
                        border: 1px solid #F44336; margin-bottom: 1rem;'>
                <span style='font-size: 1.1rem;'>⚠️ <strong style='color: #F44336;'>
                    Attendance Alert</strong></span><br>
                <span style='color: #ccc; font-size: 0.9rem;'>
                    {att_status['status']} — Attendance rate: {att_status['attendance_rate']}%
                    {f" | Absent {att_status['absence_streak']} consecutive days" if att_status['absence_streak'] > 0 else ""}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("🩹 Generate Recovery Plan", type="primary", key="recovery_btn"):
            with st.spinner("Creating personalized catch-up plan..."):
                plan = generate_recovery_plan(selected_id)
                st.session_state[f"recovery_plan_{selected_id}"] = plan

        if f"recovery_plan_{selected_id}" in st.session_state:
            st.markdown(st.session_state[f"recovery_plan_{selected_id}"])

    # ----- Attendance Section -----
    st.markdown("---")
    st.markdown("### 📅 Record Attendance")
    att_col1, att_col2, att_col3 = st.columns(3)
    with att_col1:
        att_date = st.date_input("Date", value=date.today())
    with att_col2:
        att_present = st.radio("Status", ["Present", "Absent"], horizontal=True)
    with att_col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Record", use_container_width=True):
            record_attendance(selected_id, att_date.isoformat(), att_present == "Present")
            st.success(f"Recorded: {att_present} on {att_date}")
            st.rerun()

    # Attendance history visualization (Feature 2)
    history = get_attendance_history(selected_id, days=30)
    if history:
        with st.expander("📅 Attendance History (Last 30 Days)", expanded=False):
            for record in history[:15]:
                icon = "✅" if record["present"] else "❌"
                color = "#4CAF50" if record["present"] else "#F44336"
                st.markdown(
                    f"<span style='color: {color};'>{icon} {record['date']}</span>",
                    unsafe_allow_html=True,
                )

    # ----- Feature 4: Performance Evolution -----
    if trend["overall_trend"] != "insufficient_data":
        st.markdown("---")
        st.markdown("### 📈 Performance Evolution")

        # Trend summary
        st.markdown(trend["summary"])

        # Topic trend details
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

        # AI Performance Feedback button
        if st.button("🧠 Get AI Performance Feedback", key="perf_feedback_btn"):
            with st.spinner("Analyzing performance trajectory..."):
                feedback = generate_performance_feedback(selected_id)
                st.session_state[f"perf_feedback_{selected_id}"] = feedback

        if f"perf_feedback_{selected_id}" in st.session_state:
            st.markdown(st.session_state[f"perf_feedback_{selected_id}"])

    # ----- Topic Performance -----
    if topic_scores:
        st.markdown("---")
        st.markdown("### 📊 Topic Performance")

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

    # ----- Personalized Learning Path -----
    st.markdown("---")
    st.markdown("### 🎯 Personalized Learning Path")

    if st.button("🧠 Generate Learning Path", type="primary", use_container_width=True):
        with st.spinner("Analyzing your performance and creating a plan..."):
            available = []
            if vectorstore_exists():
                try:
                    available = get_available_topics()
                except Exception:
                    pass

            path = generate_learning_path(selected_id, available)
            st.session_state[f"learning_path_{selected_id}"] = path

    if f"learning_path_{selected_id}" in st.session_state:
        st.markdown(st.session_state[f"learning_path_{selected_id}"])

    # ----- Doubt Solving -----
    st.markdown("---")
    st.markdown("### 💬 Ask a Doubt")

    if not vectorstore_exists():
        st.warning("Upload a curriculum PDF first to enable doubt-solving.")
    else:
        doubt_question = st.text_area(
            "Type your question here:",
            placeholder="e.g., What is Newton's Second Law and how is it applied?",
            height=100,
        )

        if st.button("🔍 Get Answer", type="primary"):
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
