# backend/ui_styles.py
"""
Global CSS injection for MTRX-TriAxis Streamlit app.
Import and call inject_global_styles() once in app.py.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
/* ── Google Font ─────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ──────────────────────────────────── */
:root {
    --bg:        #0A0C14;
    --surface:   #12151F;
    --surface2:  #1A1D2E;
    --border:    #252840;
    --accent:    #7C6FFF;
    --accent2:   #A78BFA;
    --success:   #22C55E;
    --warning:   #F59E0B;
    --danger:    #EF4444;
    --text:      #E8EAF0;
    --muted:     #6B7280;
    --radius:    12px;
}

/* ── Global Font ─────────────────────────────────────── */
html, body, [class*="css"], .stMarkdown, .stText, p, h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
}

/* ── Main Layout ─────────────────────────────────────── */
.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0F1A 0%, #12151F 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text);
}

/* Sidebar nav items */
[data-testid="stSidebar"] button[kind="secondary"] {
    border-radius: 8px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background: var(--surface2) !important;
    transform: translateX(3px);
}

/* Active nav item */
[data-testid="stSidebar"] [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,111,255,0.2), rgba(167,139,250,0.1)) !important;
    border-left: 3px solid var(--accent) !important;
}

/* ── Buttons ─────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7C6FFF, #A78BFA) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    color: white !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(124,111,255,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,111,255,0.5) !important;
    filter: brightness(1.1) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0px) !important;
}
.stButton > button[kind="secondary"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    color: var(--accent2) !important;
}

/* ── Metric Cards ────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, var(--surface), var(--surface2)) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem 1.2rem !important;
    transition: border-color 0.2s ease, transform 0.2s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
    transform: translateY(-2px);
}
[data-testid="stMetricLabel"] {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
}

/* ── Input Fields ────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput input,
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,111,255,0.15) !important;
}

/* ── Expanders ───────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stExpander"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: var(--text) !important;
}

/* ── Dataframe ───────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7C6FFF, #A78BFA) !important;
    color: white !important;
    font-weight: 600 !important;
}

/* ── Alerts / Info boxes ─────────────────────────────── */
.stAlert {
    border-radius: var(--radius) !important;
    border-width: 1px !important;
}
[data-testid="stToast"] {
    border-radius: var(--radius) !important;
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
}

/* ── Progress Bar ────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, #7C6FFF, #A78BFA) !important;
    border-radius: 10px !important;
}

/* ── Dividers ────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ── Select Slider ───────────────────────────────────── */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--accent) !important;
    border: 3px solid var(--accent2) !important;
}

/* ── Status badges (success/error in sidebar) ────────── */
[data-testid="stSidebar"] .stSuccess {
    background: rgba(34,197,94,0.1) !important;
    border: 1px solid rgba(34,197,94,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stInfo {
    background: rgba(124,111,255,0.1) !important;
    border: 1px solid rgba(124,111,255,0.3) !important;
    border-radius: 8px !important;
}

/* ── Form submit button ──────────────────────────────── */
[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(135deg, #7C6FFF, #A78BFA) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    color: white !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(124,111,255,0.3) !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,111,255,0.5) !important;
}

/* ── Scrollbar ───────────────────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg);
}
::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent);
}

/* ── Spinner ─────────────────────────────────────────── */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* ── Page link  ──────────────────────────────────────── */
.stPageLink a {
    color: var(--accent2) !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}
</style>
"""


def inject_global_styles() -> None:
    """Inject global CSS into the Streamlit app. Call once from app.py."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
