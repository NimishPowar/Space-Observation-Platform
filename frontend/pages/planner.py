"""Observation planner page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import (
    render_error,
    render_loading_state,
    render_location_selector,
    render_metrics,
    render_section_heading,
    render_status,
    render_table,
    render_time_selector,
)


def _star_rating(score: float) -> str:
    rounded = int(round(score / 20))
    return "★" * max(1, min(5, rounded)) + "☆" * max(0, 5 - max(1, min(5, rounded)))


def _build_event_rows(events: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for event in events or []:
        rows.append(
            {
                "Event": event.get("name", "N/A"),
                "Category": event.get("category", "N/A"),
                "Starts": event.get("start_time", "N/A"),
                "Type": event.get("event_type", "N/A"),
            }
        )
    return rows


def render() -> None:
    """Render the observation planner page with a city-first workflow and event recommendations."""
    st.title("Observation Planner")
    st.caption("What should I observe tonight?")

    latitude, longitude, location_label = render_location_selector()
    timestamp = render_time_selector()
    limit = st.slider("How many recommendations?", min_value=1, max_value=10, value=5)

    if not st.button("Plan observation"):
        return

    client = ApiClient()
    try:
        scores = events = None

        def load_data() -> None:
            nonlocal scores, events
            scores = client.get_planner(
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                elevation=0.0,
                limit=limit,
            )
            try:
                events = client.get_events(
                    latitude=latitude,
                    longitude=longitude,
                    timestamp=timestamp,
                    limit=min(3, limit),
                )
            except FrontendApiError:
                events = None

        render_loading_state(load_data)
        render_status(f"Observation plan prepared for {location_label}.", kind="success")
        render_metrics(
            [
                ("Location", location_label),
                ("Tonight", str(limit)),
                ("Best object", (scores or [{}])[0].get("object_name", "N/A")),
            ]
        )

        render_section_heading("Best Observation Opportunities")
        for score in scores or []:
            visibility_window = score.get("visibility_window") or {}
            st.markdown(
                f"### {_star_rating(float(score.get('score', 0)))} {score.get('object_name', 'Observation')}"
            )
            st.write(score.get("score_reason", "Observation opportunity available."))
            st.caption(
                f"Best Time: {visibility_window.get('start', 'N/A')} → {visibility_window.get('end', 'N/A')}"
            )
            st.markdown("---")

        render_section_heading("Upcoming Celestial Events")
        if events:
            render_table(_build_event_rows(events))
        else:
            st.info("Upcoming celestial event details are temporarily unavailable.")
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
