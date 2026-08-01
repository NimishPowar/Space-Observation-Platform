"""Common Streamlit UI helpers for the frontend application."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Callable

import pandas as pd
import streamlit as st


def render_section_heading(title: str) -> None:
    """Render a simple heading for a page section."""
    st.subheader(title)


def render_status(message: str, *, kind: str = "info") -> None:
    """Render a consistent inline status message for the page."""
    if kind == "success":
        st.success(message)
    elif kind == "warning":
        st.warning(message)
    elif kind == "error":
        st.error(message)
    else:
        st.info(message)


def render_error(message: str) -> None:
    """Render a backend or validation error with a clear style."""
    st.error(message)


def render_loading_state(action: Callable[[], None]) -> None:
    """Show a spinner while an operation is in progress."""
    with st.spinner("Loading data..."):
        action()


def render_metrics(items: list[tuple[str, str]]) -> None:
    """Render a set of key-value metrics as simple cards."""
    if not items:
        return

    columns = st.columns(len(items))
    for column, (title, value) in zip(columns, items):
        column.metric(title, value)


def render_table(records: list[dict]) -> None:
    """Render a list of dictionaries as a streamlit-friendly table."""
    if not records:
        st.info("No records available for display.")
        return

    dataframe = pd.DataFrame.from_records(records)
    st.dataframe(dataframe, use_container_width=True, hide_index=True)


def render_location_selector() -> tuple[float, float, str]:
    """Render a global city selector in the sidebar and persist the selected coordinates in session state."""
    from frontend.client import ApiClient, FrontendApiError

    city_query = st.session_state.get("location_query", "Mumbai")
    location_label = st.session_state.get("location_label", "Mumbai")
    latitude = float(st.session_state.get("location_latitude", 12.5))
    longitude = float(st.session_state.get("location_longitude", 77.5))

    with st.sidebar:
        st.subheader("Current Location")
        new_query = st.text_input("Search city", value=city_query, key="location_query")
        if st.button("Resolve city"):
            try:
                client = ApiClient()
                match = client.search_city(new_query)[0]
                latitude = float(match["lat"])
                longitude = float(match["lon"])
                location_label = match.get("display_name", new_query)
                st.session_state["location_latitude"] = latitude
                st.session_state["location_longitude"] = longitude
                st.session_state["location_label"] = location_label
                st.success(f"Location set to {location_label}.")
            except FrontendApiError as exc:
                st.error(str(exc))

        st.caption(f"📍 {location_label}")

    return latitude, longitude, location_label


def render_time_selector() -> str | None:
    """Render a friendly time selection widget and return an ISO 8601 string."""
    when_mode = st.radio("When?", ["Right Now", "Tonight", "Pick Date & Time"], horizontal=True)

    if when_mode == "Right Now":
        return datetime.now(timezone.utc).isoformat()

    if when_mode == "Tonight":
        tonight = datetime.now(timezone.utc).replace(hour=20, minute=30, second=0, microsecond=0)
        if tonight < datetime.now(timezone.utc):
            tonight += timedelta(days=1)
        return tonight.isoformat()

    selected_date = st.date_input("Date", value=date.today())
    selected_time = st.time_input("Time", value=time(20, 30))
    selected_dt = datetime.combine(selected_date, selected_time, tzinfo=timezone.utc)
    return selected_dt.isoformat()
