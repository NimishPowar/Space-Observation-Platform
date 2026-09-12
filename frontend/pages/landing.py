"""Landing splash screen for the Space Observation Intelligence Platform."""

from __future__ import annotations

import base64
from pathlib import Path
import streamlit as st

from frontend.ui import inject_astronomy_styles


def _get_landing_bg_url() -> str:
    """Return base64 data URL or HTTP URL for the landing page background image."""
    img_path = Path(__file__).resolve().parent.parent / "images" / "landing_page.jpg"
    if img_path.is_file():
        try:
            encoded = base64.b64encode(img_path.read_bytes()).decode("utf-8")
            return f"data:image/jpeg;base64,{encoded}"
        except Exception:
            pass

    return "http://127.0.0.1:8000/static/images/landing_page.jpg"


def render_landing() -> None:
    """Render full-bleed hero landing screen with space photo background overlay and navigation cards."""
    inject_astronomy_styles(is_landing=True)
    bg_url = _get_landing_bg_url()

    # Apply dimmed space photo background and centered hero card styling
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        .stApp {{
            background-image: linear-gradient(rgba(5, 6, 9, 0.72), rgba(5, 6, 9, 0.88)), url('{bg_url}') !important;
            background-size: cover !important;
            background-position: center center !important;
            background-attachment: fixed !important;
        }}

        /* Hero text container */
        .hero-header {{
            text-align: center;
            padding: 60px 20px 40px 20px;
            max-width: 900px;
            margin: 0 auto;
        }}

        .hero-title {{
            font-family: 'Orbitron', sans-serif !important;
            font-size: 3.5rem !important;
            font-weight: 800 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.14em !important;
            text-shadow: 0 0 35px rgba(56, 189, 248, 0.5);
            background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 40%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 !important;
            line-height: 1.25 !important;
        }}

        .hero-subtitle {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.22em !important;
            color: #94a3b8 !important;
            margin-top: 14px !important;
            margin-bottom: 40px !important;
        }}

        /* Equal Sized 3-Card Container Grid Layout */
        div[data-testid="stHorizontalBlock"],
        div[data-testid="horizontal-block"] {{
            display: flex !important;
            flex-direction: row !important;
            justify-content: center !important;
            align-items: center !important;
            width: 100% !important;
            max-width: 1050px !important;
            margin: 0 auto !important;
            gap: 28px !important;
        }}

        div[data-testid="column"],
        div[data-testid="stColumn"] {{
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            flex: 0 0 300px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }}

        /* Custom Card Buttons Styling */
        div[data-testid="column"] div.stButton,
        div[data-testid="stColumn"] div.stButton {{
            width: 300px !important;
            display: flex !important;
            justify-content: center !important;
        }}

        div[data-testid="column"] div.stButton > button,
        div[data-testid="stColumn"] div.stButton > button {{
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            height: 210px !important;
            min-height: 210px !important;
            max-height: 210px !important;
            box-sizing: border-box !important;
            background: rgba(15, 23, 42, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 20px !important;
            padding: 24px 16px !important;
            backdrop-filter: blur(16px) !important;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
        }}

        div[data-testid="column"] div.stButton > button:hover,
        div[data-testid="stColumn"] div.stButton > button:hover {{
            background: rgba(56, 189, 248, 0.15) !important;
            border-color: #38bdf8 !important;
            transform: translateY(-6px) scale(1.02) !important;
            box-shadow: 0 16px 45px rgba(56, 189, 248, 0.35) !important;
        }}

        div[data-testid="column"] div.stButton > button p,
        div[data-testid="stColumn"] div.stButton > button p {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-size: 1.05rem !important;
            color: #e2e8f0 !important;
            margin: 0 !important;
            line-height: 1.6 !important;
        }}
        </style>

        <div class="hero-header">
            <h1 class="hero-title">SPACE OBSERVATION</h1>
            <div class="hero-subtitle">INTELLIGENCE PLATFORM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3 Horizontal Navigation Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔭\n\nEXPLORE\n\nReal-time 2D Night Sky Map & Ephemeris", key="landing_btn_explore"):
            st.session_state["selected_page"] = "🌟 Explore"
            st.rerun()

    with col2:
        if st.button("🎯\n\nPLANNER\n\nTarget Scoring & NASA APOD", key="landing_btn_planner"):
            st.session_state["selected_page"] = "🔭 Planner"
            st.rerun()

    with col3:
        if st.button("💡\n\nDISCOVERY\n\n3D Simulators & Astronomy Basics", key="landing_btn_discovery"):
            st.session_state["selected_page"] = "💡 Discovery"
            st.rerun()
