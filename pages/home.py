"""
MTRX-TriAxis | Home Page
Welcome page with project overview and quick-start guide.
"""

import streamlit as st

# ----- Hero Section -----
st.markdown(
    """
    <div style='text-align: center; padding: 2rem 0 1rem 0;'>
        <span style='font-size: 4rem;'>🎓</span>
        <h1 style='margin-bottom: 0; color: #6C63FF;'>MTRX-TriAxis</h1>
        <p style='font-size: 1.3rem; color: #aaa; margin-top: 0.5rem;'>
            AI-Powered Classroom Assistant
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ----- Feature Cards -----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>📄</span>
            <h3 style='color: #6C63FF;'>Smart PDF Processing</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                Upload curriculum PDFs and let AI extract, clean, and chunk
                the content into study-ready units.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>🧠</span>
            <h3 style='color: #6C63FF;'>RAG-Powered Learning</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                Ask doubts and get accurate answers grounded in your
                curriculum using retrieval-augmented generation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>📝</span>
            <h3 style='color: #6C63FF;'>Smart Quizzes</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                Auto-generate MCQ quizzes from your curriculum.
                Track scores and identify weak areas automatically.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>🎯</span>
            <h3 style='color: #6C63FF;'>Personalized Paths</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                AI analyzes each student's performance to create
                customized learning paths that target their weak spots.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col5:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>👩‍🏫</span>
            <h3 style='color: #6C63FF;'>Teacher Insights</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                Dashboard with class analytics, weak topic detection,
                and AI-generated teaching suggestions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col6:
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #1a1d29, #2a2d3a);
                    border-radius: 12px; padding: 1.5rem; border: 1px solid #333;
                    min-height: 200px;'>
            <span style='font-size: 2rem;'>🌤️</span>
            <h3 style='color: #6C63FF;'>Context Aware</h3>
            <p style='color: #ccc; font-size: 0.9rem;'>
                Weather-based teaching suggestions — adjusts
                recommendations for rainy days, heat, and more.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----- Quick Start Guide -----
st.markdown("---")
st.markdown("## 🚀 Quick Start Guide")

st.markdown(
    """
    <div style='background: #1a1d29; border-radius: 10px; padding: 1.5rem;
                border-left: 4px solid #6C63FF;'>
    <ol style='color: #ccc; line-height: 2;'>
        <li><strong>Upload Curriculum</strong> — Go to the <em>Upload Curriculum</em> page and upload a PDF textbook</li>
        <li><strong>Add Students</strong> — Register students in the <em>Student View</em> page</li>
        <li><strong>Take Quizzes</strong> — Generate topic-based quizzes in the <em>Quiz</em> page</li>
        <li><strong>Ask Doubts</strong> — Students can ask questions about the curriculum</li>
        <li><strong>Review Insights</strong> — Teachers check the <em>Dashboard</em> for class analytics</li>
    </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----- Prerequisites -----
st.markdown("---")
st.markdown("### ⚙️ Prerequisites")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown(
        """
        **Ollama** (Local LLM runtime)
        ```bash
        # Install Ollama
        curl -fsSL https://ollama.com/install.sh | sh

        # Pull required models
        ollama pull mistral
        ollama pull nomic-embed-text

        # Start Ollama
        ollama serve
        ```
        """
    )

with col_b:
    st.markdown(
        """
        **Python Dependencies**
        ```bash
        pip install -r requirements.txt
        ```

        **Environment Variables**
        ```bash
        cp .env.example .env
        # Edit .env with your OpenWeatherMap API key
        ```
        """
    )
