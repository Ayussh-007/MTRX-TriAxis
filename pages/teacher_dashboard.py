"""
MTRX-TriAxis | Teacher Dashboard
Class analytics, teacher feedback & style adaptation, weather-aware suggestions,
class weakness detection, and auto-generated doubt sheets.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
from dotenv import load_dotenv

from backend.teacher_insights import (
    get_class_performance,
    get_weak_topics_across_class,
    get_strong_topics_across_class,
    generate_teaching_suggestions,
)
from backend.teacher_feedback import (
    add_feedback, get_recent_feedback, set_preference,
    get_all_preferences, build_style_context,
    analyze_feedback_with_llm, TEACHING_STYLES, CLASS_PACE,
    get_preference,
)
from backend.attendance_intelligence import get_frequently_absent_students
from backend.class_weakness import get_top_weak_topics, generate_doubt_sheet
from backend.weather_context import get_weather_summary, get_weather, is_bad_weather

load_dotenv()

st.markdown("# 👩‍🏫 Teacher Dashboard")
st.markdown("Class analytics, feedback, insights, and AI-powered teaching suggestions.")
st.markdown("---")

# ----- Weather Context Bar (Feature 3) -----
weather_city = os.getenv("WEATHER_CITY", "Mumbai")
weather_data = get_weather(weather_city)
weather_summary = get_weather_summary(weather_city)

# Enhanced weather bar with bad-weather warnings
if weather_data and is_bad_weather(weather_data):
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, #b71c1c, #880e4f);
                    border-radius: 10px; padding: 0.8rem 1.2rem;
                    margin-bottom: 1rem; border: 1px solid #f44336;'>
            <span style='font-size: 0.9rem; color: #ffcdd2;'>
                ⚠️ <strong>Bad Weather Alert:</strong> {weather_summary}
            </span><br>
            <span style='font-size: 0.8rem; color: #ef9a9a;'>
                💡 Consider lighter teaching, revision focus, or recorded material today.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, #1a237e, #283593);
                    border-radius: 10px; padding: 0.8rem 1.2rem;
                    margin-bottom: 1rem; border: 1px solid #3949ab;'>
            <span style='font-size: 0.9rem; color: #e8eaf6;'>{weather_summary}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =================================================================
# FEATURE 1: Teacher Feedback & Style Preferences
# =================================================================
st.markdown("### 🎨 Teaching Style & Feedback")

pref_col1, pref_col2 = st.columns(2)

with pref_col1:
    st.markdown("#### Set Preferences")

    # Teaching style selector
    current_style = get_preference("teaching_style", "visual")
    style_options = list(TEACHING_STYLES.keys())
    selected_style = st.selectbox(
        "Teaching Style:",
        options=style_options,
        index=style_options.index(current_style) if current_style in style_options else 0,
        format_func=lambda x: f"{x.title()} — {TEACHING_STYLES[x][:40]}...",
    )

    # Class pace
    current_pace = get_preference("class_pace", "normal")
    pace_options = list(CLASS_PACE.keys())
    selected_pace = st.selectbox(
        "Class Pace:",
        options=pace_options,
        index=pace_options.index(current_pace) if current_pace in pace_options else 1,
        format_func=lambda x: f"{x.title()} — {CLASS_PACE[x][:40]}...",
    )

    # Difficulty level
    current_diff = get_preference("difficulty_level", "medium")
    selected_diff = st.select_slider(
        "Content Difficulty:",
        options=["easy", "medium", "hard"],
        value=current_diff if current_diff in ["easy", "medium", "hard"] else "medium",
    )

    if st.button("💾 Save Preferences", type="primary"):
        set_preference("teaching_style", selected_style)
        set_preference("class_pace", selected_pace)
        set_preference("difficulty_level", selected_diff)
        st.success("✅ Preferences saved! AI outputs will adapt accordingly.")

with pref_col2:
    st.markdown("#### Quick Feedback")

    # Quick feedback buttons
    fb_col1, fb_col2 = st.columns(2)
    with fb_col1:
        if st.button("😰 Students Struggling", use_container_width=True):
            add_feedback("Students are struggling with current topics", "struggle")
            st.toast("Feedback recorded!")
        if st.button("🏃 Class Too Fast", use_container_width=True):
            add_feedback("Class pace is too fast for most students", "pace")
            st.toast("Feedback recorded!")
    with fb_col2:
        if st.button("👁️ Need More Visuals", use_container_width=True):
            add_feedback("Students respond better to visual teaching aids", "style")
            st.toast("Feedback recorded!")
        if st.button("✅ Class Doing Well", use_container_width=True):
            add_feedback("Class is performing well, students are engaged", "positive")
            st.toast("Feedback recorded!")

    # Custom feedback input
    custom_feedback = st.text_input(
        "Custom feedback:",
        placeholder="e.g., 'Group B needs extra help with calculus'",
    )
    if st.button("📝 Submit Feedback") and custom_feedback.strip():
        add_feedback(custom_feedback.strip(), "general")
        st.success("✅ Feedback recorded!")

    # Show recent feedback
    recent = get_recent_feedback(limit=5)
    if recent:
        with st.expander("📋 Recent Feedback", expanded=False):
            for f in recent:
                badge_colors = {
                    "struggle": "#F44336", "pace": "#FF9800",
                    "style": "#2196F3", "positive": "#4CAF50", "general": "#9E9E9E",
                }
                color = badge_colors.get(f["category"], "#9E9E9E")
                st.markdown(
                    f"<span style='color: {color};'>●</span> "
                    f"_{f['feedback_text']}_ "
                    f"<span style='color: #666; font-size: 0.75rem;'>({f['category']})</span>",
                    unsafe_allow_html=True,
                )

st.markdown("---")

# ----- Class Overview Metrics -----
performance = get_class_performance()

if performance["num_students"] == 0:
    st.info("No students registered yet. Add students and take quizzes to see analytics.")
    st.stop()

st.markdown("### 📊 Class Overview")

m1, m2, m3, m4 = st.columns(4)
m1.metric("👥 Students", performance["num_students"])
m2.metric("📈 Class Average", f"{performance['class_avg']}%")
m3.metric("📅 Avg Attendance", f"{performance['avg_attendance']}%")

weak_count = len(get_weak_topics_across_class())
m4.metric("⚠️ Weak Topics", weak_count)

st.markdown("---")

# ----- Feature 2: Frequently Absent Students -----
absent_students = get_frequently_absent_students(threshold=70.0)
if absent_students:
    st.markdown("### 🚨 Attendance Alerts")
    for s in absent_students:
        streak_warning = f" | 🔥 Absent {s['absence_streak']} days in a row" if s["absence_streak"] >= 2 else ""
        severity_color = "#F44336" if s["attendance_rate"] < 50 else "#FF9800"

        st.markdown(
            f"""
            <div style='background: #1a1d29; padding: 0.7rem 1rem; border-radius: 8px;
                        margin-bottom: 0.4rem; border-left: 4px solid {severity_color};
                        display: flex; justify-content: space-between; align-items: center;'>
                <span>🧑‍🎓 <strong>{s['name']}</strong>
                    <span style='color: #888;'>{streak_warning}</span>
                </span>
                <span style='color: {severity_color}; font-weight: bold;'>
                    {s['attendance_rate']}% attendance
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")

# ----- Per-Student Performance Table -----
st.markdown("### 👥 Student Performance")

if performance["per_student"]:
    df_students = pd.DataFrame(performance["per_student"])
    df_students.columns = ["ID", "Name", "Overall Score (%)", "Attendance (%)"]

    st.dataframe(
        df_students.style.background_gradient(
            subset=["Overall Score (%)"],
            cmap="RdYlGn",
            vmin=0,
            vmax=100,
        ).background_gradient(
            subset=["Attendance (%)"],
            cmap="RdYlGn",
            vmin=0,
            vmax=100,
        ),
        use_container_width=True,
        hide_index=True,
    )

# ----- Topic Performance Charts -----
if performance["topic_breakdown"]:
    st.markdown("---")
    st.markdown("### 📊 Topic Performance")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        topics = list(performance["topic_breakdown"].keys())
        averages = [data["average"] for data in performance["topic_breakdown"].values()]
        student_counts = [data["students_tested"] for data in performance["topic_breakdown"].values()]

        colors = []
        for avg in averages:
            if avg >= 70:
                colors.append("#4CAF50")
            elif avg >= 50:
                colors.append("#FF9800")
            else:
                colors.append("#F44336")

        fig_bar = go.Figure(data=[
            go.Bar(
                x=topics,
                y=averages,
                marker_color=colors,
                text=[f"{a}%" for a in averages],
                textposition="auto",
            )
        ])
        fig_bar.update_layout(
            title="Average Score by Topic",
            xaxis_title="Topic",
            yaxis_title="Average Score (%)",
            yaxis_range=[0, 100],
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1a1d29",
            height=400,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        fig_pie = px.pie(
            names=topics,
            values=student_counts,
            title="Quiz Participation by Topic",
            hole=0.4,
        )
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1a1d29",
            height=400,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# =================================================================
# FEATURE 5: Class Weakness Detection + Doubt Sheet
# =================================================================
st.markdown("---")
st.markdown("### 📝 Class Weakness Analysis & Doubt Sheet")

top_weak = get_top_weak_topics(top_n=5)
if top_weak:
    st.markdown("**Top Weak Topics (by severity):**")
    for i, w in enumerate(top_weak):
        severity_bar_width = min(w["severity"] * 10, 100)
        severity_color = "#F44336" if w["class_avg"] < 30 else "#FF9800" if w["class_avg"] < 50 else "#FFC107"

        st.markdown(
            f"""
            <div style='background: #1a1d29; padding: 0.6rem 1rem; border-radius: 8px;
                        margin-bottom: 0.4rem; display: flex; justify-content: space-between;
                        align-items: center;'>
                <span>
                    <strong style='color: {severity_color};'>#{i+1}</strong>
                    {w['topic']}
                    <span style='color: #666; font-size: 0.8rem;'>
                        — {w['students_struggling']}/{w['total_students']} students struggling
                    </span>
                </span>
                <span style='color: {severity_color}; font-weight: bold;'>
                    {w['class_avg']}% avg
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Generate doubt sheet button
    if st.button("📋 Generate Doubt Resolution Sheet", type="primary", use_container_width=True):
        weak_topic_names = [w["topic"] for w in top_weak[:3]]
        with st.spinner(f"Generating doubt sheet for: {', '.join(weak_topic_names)}..."):
            sheet = generate_doubt_sheet(weak_topic_names)
            st.session_state["doubt_sheet"] = sheet

    if "doubt_sheet" in st.session_state:
        st.markdown(st.session_state["doubt_sheet"])
else:
    st.info("No weak topics detected. Students are performing well across all topics!")

# ----- AI Teaching Suggestions (enhanced with style context) -----
st.markdown("---")
st.markdown("### 🧠 AI Teaching Suggestions")

# Show active style context
style_ctx = build_style_context()
if style_ctx and "No teacher preferences" not in style_ctx:
    with st.expander("🎨 Active Teaching Style Context", expanded=False):
        st.code(style_ctx, language=None)

suggestion_city = st.text_input(
    "City for weather context (optional):",
    value=weather_city,
    help="Include weather data to get context-aware teaching suggestions.",
)

if st.button("💡 Generate Teaching Suggestions", type="primary", use_container_width=True):
    with st.spinner("Analyzing class performance and generating suggestions..."):
        suggestions = generate_teaching_suggestions(city=suggestion_city if suggestion_city else None)
        st.session_state["teacher_suggestions"] = suggestions

if "teacher_suggestions" in st.session_state:
    st.markdown(st.session_state["teacher_suggestions"])

# ----- Feedback Analysis (Feature 1) -----
recent_fb = get_recent_feedback(limit=5)
if recent_fb:
    st.markdown("---")
    st.markdown("### 🔍 AI Feedback Analysis")

    if st.button("🧠 Analyze My Feedback", use_container_width=True):
        with st.spinner("Analyzing your feedback patterns..."):
            analysis = analyze_feedback_with_llm()
            st.session_state["feedback_analysis"] = analysis

    if "feedback_analysis" in st.session_state:
        st.markdown(st.session_state["feedback_analysis"])
