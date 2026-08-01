"""Observation planner page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import (
    render_error,
    render_loading_state,
    render_metrics,
    render_section_heading,
    render_status,
    render_table,
)


def _build_score_rows(scores: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for score in scores or []:
        visibility_window = score.get("visibility_window") or {}
        rows.append(
            {
                "Object": score.get("object_name", "N/A"),
                "Score": f"{score.get('score', 0):.2f}",
                "Reason": score.get("score_reason", "N/A"),
                "Window start": visibility_window.get("start", "N/A"),
                "Window end": visibility_window.get("end", "N/A"),
                "Description": visibility_window.get("description", "N/A"),
            }
        )
    return rows


def render() -> None:
    """Render the observation planner page."""
    st.title("Observation Planner")
    st.caption("Use a city search to resolve coordinates and rank the best observation windows.")

    with st.form("planner_form"):
        city_search = st.text_input("City search", value="Mumbai")
        timestamp = st.text_input("Timestamp (optional ISO 8601)", value="")
        elevation = st.number_input("Elevation (meters)", value=0.0, step=1.0)
        limit = st.slider("Limit", min_value=1, max_value=10, value=5)
        with st.expander("Advanced"):
            latitude = st.number_input("Latitude", value=12.5, min_value=-90.0, max_value=90.0, step=0.1)
            longitude = st.number_input("Longitude", value=77.5, min_value=-180.0, max_value=180.0, step=0.1)
        submitted = st.form_submit_button("Plan observation")

    if not submitted:
        return

    client = ApiClient()
    try:
        scores = None
        resolved_latitude = latitude
        resolved_longitude = longitude
        location_label = "manual coordinates"

        def load_data() -> None:
            nonlocal scores, resolved_latitude, resolved_longitude, location_label
            if city_search.strip():
                city_matches = client.search_city(city_search)
                selected_match = city_matches[0]
                resolved_latitude = float(selected_match["lat"])
                resolved_longitude = float(selected_match["lon"])
                location_label = selected_match.get("display_name", city_search)

            scores = client.get_planner(
                latitude=resolved_latitude,
                longitude=resolved_longitude,
                timestamp=timestamp or None,
                elevation=elevation,
                limit=limit,
            )

        render_loading_state(load_data)
        render_status(f"Observation plan prepared for {location_label}.", kind="success")
        render_metrics(
            [
                ("Latitude", f"{resolved_latitude:.3f}"),
                ("Longitude", f"{resolved_longitude:.3f}"),
                ("Ranked windows", str(limit)),
            ]
        )

        render_section_heading("Planning results")
        render_table(_build_score_rows(scores))
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
