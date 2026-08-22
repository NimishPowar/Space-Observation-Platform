"""Frontend application entrypoint for the Streamlit UI."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st

from frontend.ui import inject_astronomy_styles
from frontend.pages.discovery import render as render_discovery
from frontend.pages.explore import render as render_explore
from frontend.pages.planner import render as render_planner


def render_top_navbar(pages: dict) -> str:
    """Render a modern top navigation bar with brand logo and horizontal nav pills."""
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(
            """
            <div style="display:flex; align-items:center; gap:12px; padding: 4px 0;">
                <span style="font-size:2.2rem; filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.6));">🌌</span>
                <div>
                    <div style="font-family:'Outfit',sans-serif; font-size:1.45rem; font-weight:800; letter-spacing:-0.03em; background: linear-gradient(135deg, #ffffff 0%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        SPACE OBSERVATION PLATFORM
                    </div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:0.72rem; color:#94a3b8; letter-spacing:0.12em; text-transform:uppercase;">
                        Real-time Ephemeris & Observation Intelligence
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        selected_page = st.radio(
            "Navigation",
            list(pages.keys()),
            horizontal=True,
            label_visibility="collapsed",
            key="top_nav_selection",
        )

    st.markdown("<hr style='margin-top: 4px; margin-bottom: 24px; opacity: 0.15;'>", unsafe_allow_html=True)
    return selected_page


def run() -> None:
    """Run the Streamlit UI with a top navbar navigation flow."""
    st.set_page_config(
        page_title="Space Observation Intelligence Platform",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_astronomy_styles()

    pages = {
        "🌟 Explore": render_explore,
        "🔭 Planner": render_planner,
        "💡 Discovery": render_discovery,
    }

    selected_page_name = render_top_navbar(pages)
    pages[selected_page_name]()


if __name__ == "__main__":
    run()
