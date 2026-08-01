"""Home page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.ui import render_metrics, render_status


def render() -> None:
    """Render the home page with a simple overview of the available features."""
    st.title("Space Observation Intelligence Platform")
    st.caption("A function-first interface for exploring astronomy, planning observations, and reviewing educational data.")

    render_status(
        "Use the sidebar to move between Home, Explore, Observation Planner, Events, and Learn.",
        kind="info",
    )

    render_metrics(
        [
            ("Explore", "Realtime astronomy summary"),
            ("Planner", "Observation scoring"),
            ("Events", "Celestial event lookup"),
            ("Learn", "Educational content"),
        ]
    )

    st.subheader("Available workflow")
    st.markdown(
        "- Search a city to resolve coordinates automatically.\n"
        "- Review the sky context using the Explore page.\n"
        "- Rank observation opportunities using the Planner page.\n"
        "- Browse events and educational content from the backend data layer."
    )


if __name__ == "__main__":
    render()
