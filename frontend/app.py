"""Frontend application entrypoint for the Streamlit UI."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import streamlit as st

from frontend.pages.discovery import render as render_discovery
from frontend.pages.explore import render as render_explore
from frontend.pages.planner import render as render_planner


def run() -> None:
    """Run the Streamlit UI with a user-focused navigation flow."""
    st.set_page_config(page_title="Space Observation Intelligence Platform", layout="wide")
    pages = {
        "Explore": render_explore,
        "Planner": render_planner,
        "Discovery": render_discovery,
    }
    selected_page = st.sidebar.radio("Navigation", list(pages.keys()), index=0)
    pages[selected_page]()


if __name__ == "__main__":
    run()
