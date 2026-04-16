"""
MTRX-TriAxis | AI-Powered Classroom Assistant
Main Streamlit entrypoint with multi-page navigation.
"""

import streamlit as st

# ----- Page Configuration -----
st.set_page_config(
    page_title="MTRX-TriAxis | AI Classroom Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----- Initialize Database on First Run -----
if "db_initialized" not in st.session_state:
    from backend.student_model import init_database
    init_database()
    st.session_state.db_initialized = True

# ----- Define Pages -----
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
pdf_page = st.Page("pages/pdf_upload.py", title="Upload Curriculum", icon="📄")
student_page = st.Page("pages/student_view.py", title="Student View", icon="🎒")
quiz_page = st.Page("pages/quiz.py", title="Quiz", icon="📝")
teacher_page = st.Page("pages/teacher_dashboard.py", title="Teacher Dashboard", icon="👩‍🏫")
agent_page = st.Page("pages/ai_agent.py", title="AI Agent", icon="🤖")

# ----- Navigation -----
pg = st.navigation(
    {
        "Main": [home_page],
        "Learning": [pdf_page, student_page, quiz_page],
        "Teaching": [teacher_page],
        "Advanced": [agent_page],
    }
)

# ----- Sidebar Branding -----
with st.sidebar:
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; padding: 1rem 0;'>
            <span style='font-size: 2rem;'>🎓</span><br>
            <span style='font-size: 1.1rem; font-weight: 700; color: #6C63FF;'>
                MTRX-TriAxis
            </span><br>
            <span style='font-size: 0.75rem; color: #888;'>
                AI Classroom Assistant
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Ollama status indicator
    from backend.llm_utils import check_ollama_connection
    if check_ollama_connection():
        st.success("🟢 Ollama Connected", icon="✅")
    else:
        st.error("🔴 Ollama Offline", icon="⚠️")
        st.caption("Run `ollama serve` in terminal")

    # Vector store status
    from backend.rag_pipeline import vectorstore_exists
    if vectorstore_exists():
        st.success("📚 Curriculum Loaded", icon="✅")
    else:
        st.info("📚 No curriculum yet", icon="ℹ️")
        st.caption("Upload a PDF to get started")

# ----- Run Selected Page -----
pg.run()
