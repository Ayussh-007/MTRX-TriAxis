"""
backend/ui_components.py
Reusable UI building blocks for MTRX-TriAxis pages.
"""

import streamlit as st


def page_header(icon: str, title: str, subtitle: str = "", accent: str = "#7C6FFF") -> None:
    """Render a consistent, styled page header."""
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, #12151F, #1A1D2E);
            border: 1px solid #252840;
            border-left: 4px solid {accent};
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        '>
            <div style='
                font-size: 2rem;
                width: 52px; height: 52px;
                background: {accent}20;
                border-radius: 12px;
                display: flex; align-items: center; justify-content: center;
                flex-shrink: 0;
            '>{icon}</div>
            <div>
                <h1 style='
                    margin:0; padding:0;
                    font-size: 1.5rem;
                    font-weight: 800;
                    color: #E8EAF0;
                    letter-spacing: -0.3px;
                    line-height: 1.2;
                '>{title}</h1>
                {"<p style='margin:0; padding:0; font-size:0.82rem; color:#6B7280; margin-top:3px;'>" + subtitle + "</p>" if subtitle else ""}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, accent: str = "#7C6FFF") -> None:
    """Render a styled section sub-heading."""
    st.markdown(
        f"""
        <div style='
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 1.4rem 0 0.8rem 0;
        '>
            <div style='width:3px; height:18px; background:{accent}; border-radius:2px;'></div>
            <span style='font-size:1rem; font-weight:700; color:#E8EAF0;'>{title}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(value: str, label: str, icon: str = "",
              color: str = "#7C6FFF", delta: str = "", delta_positive: bool = True) -> None:
    """Render a standalone stat card (use inside st.columns)."""
    delta_color = "#22C55E" if delta_positive else "#EF4444"
    delta_html = f"<div style='font-size:0.75rem; color:{delta_color}; margin-top:2px;'>{delta}</div>" if delta else ""
    st.markdown(
        f"""
        <div style='
            background: linear-gradient(135deg, #12151F, #1A1D2E);
            border: 1px solid #252840;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            text-align: center;
        '>
            <div style='font-size:1.5rem;'>{icon}</div>
            <div style='font-size:1.6rem; font-weight:800; color:{color}; margin:4px 0 2px;'>{value}</div>
            <div style='font-size:0.72rem; color:#6B7280; font-weight:600; text-transform:uppercase; letter-spacing:0.4px;'>{label}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def info_card(text: str, icon: str = "ℹ️", color: str = "#7C6FFF") -> None:
    """Render a subtle info/hint card."""
    st.markdown(
        f"""
        <div style='
            background: {color}0D;
            border: 1px solid {color}30;
            border-radius: 10px;
            padding: 0.8rem 1rem;
            display: flex;
            gap: 0.7rem;
            align-items: flex-start;
            margin: 0.6rem 0;
        '>
            <span style='font-size:1rem;'>{icon}</span>
            <span style='font-size:0.85rem; color:#D1D5DB; line-height:1.5;'>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alert_card(text: str, level: str = "warning") -> None:
    """Render a UI alert card. level: 'info' | 'warning' | 'error' | 'success'"""
    cfg = {
        "info":    ("#38BDF8", "ℹ️"),
        "warning": ("#F59E0B", "⚠️"),
        "error":   ("#EF4444", "🚨"),
        "success": ("#22C55E", "✅"),
    }
    color, icon = cfg.get(level, cfg["info"])
    st.markdown(
        f"""
        <div style='
            background: {color}10;
            border: 1px solid {color}35;
            border-radius: 10px;
            padding: 0.85rem 1rem;
            display: flex;
            gap: 0.7rem;
            align-items: flex-start;
            margin: 0.6rem 0;
        '>
            <span style='font-size:1.1rem; flex-shrink:0;'>{icon}</span>
            <span style='font-size:0.85rem; color:#E8EAF0; line-height:1.5;'>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
