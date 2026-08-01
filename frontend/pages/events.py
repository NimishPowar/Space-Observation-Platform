"""Events page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import render_error, render_loading_state, render_section_heading, render_status, render_table


def _build_event_rows(events: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for event in events or []:
        rows.append(
            {
                "Name": event.get("name", "N/A"),
                "Category": event.get("category", "N/A"),
                "Type": event.get("event_type", "N/A"),
                "Starts": event.get("start_time", "N/A"),
                "Ends": event.get("end_time", "N/A"),
                "Objects": ", ".join(event.get("visible_objects") or []),
                "Magnitude": event.get("magnitude"),
            }
        )
    return rows


def render() -> None:
    """Render the events page."""
    st.title("Events")
    st.caption("List persisted celestial events from the backend database layer.")

    with st.form("events_form"):
        timestamp = st.text_input("Timestamp (optional ISO 8601)", value="")
        limit = st.slider("Limit", min_value=1, max_value=20, value=10)
        submitted = st.form_submit_button("Load events")

    if not submitted:
        return

    client = ApiClient()
    try:
        events = None

        def load_data() -> None:
            nonlocal events
            events = client.get_events(timestamp=timestamp or None, limit=limit)

        render_loading_state(load_data)
        render_status("Event records retrieved successfully.", kind="success")
        render_section_heading("Upcoming events")
        render_table(_build_event_rows(events))
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
