"""Explore page for the Streamlit frontend."""

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


def _format_timestamp(value: object) -> str:
    if value is None:
        return "N/A"
    return str(value)


def render() -> None:
    """Render the Explore dashboard using the backend API surface."""
    st.title("Space Observation Platform")
    st.caption("Explore the night sky with a city-first workflow.")

    latitude, longitude, location_label = render_location_selector()
    timestamp = render_time_selector()
    elevation = 0.0

    client = ApiClient()
    try:
        moon = sun = planets = visibility = events = None

        def load_data() -> None:
            nonlocal moon, sun, planets, visibility, events
            moon = client.get_moon(
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                elevation=elevation,
            )
            sun = client.get_sun(
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                elevation=elevation,
            )
            planets = client.get_planets(
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                elevation=elevation,
            )
            visibility = client.get_visibility(
                latitude=latitude,
                longitude=longitude,
                timestamp=timestamp,
                elevation=elevation,
            )
            try:
                events = client.get_events(
                    latitude=latitude,
                    longitude=longitude,
                    timestamp=timestamp,
                    limit=1,
                )
            except FrontendApiError:
                events = None

        render_loading_state(load_data)
        render_status(f"📍 {location_label}", kind="info")
        render_section_heading("Sky Overview")
        render_metrics(
            [
                ("Moon Phase", moon.get("phase_name", "N/A")),
                ("Illumination", f"{(moon.get('illumination') or 0):.2%}"),
                ("Sunrise", _format_timestamp(sun.get("sunrise"))),
                ("Sunset", _format_timestamp(sun.get("sunset"))),
            ]
        )

        render_section_heading("Visible Planets")
        planet_rows = [
            {
                "Object": item.get("object_name", "N/A"),
                "Altitude": item.get("altitude"),
                "Azimuth": item.get("azimuth"),
                "Magnitude": item.get("magnitude"),
                "Visible": item.get("is_visible"),
            }
            for item in planets or []
        ]
        render_table(planet_rows)

        render_section_heading("Visibility Summary")
        best_window = (visibility or [{}])[0]
        render_metrics(
            [
                ("Best Object", best_window.get("object_name", "N/A")),
                ("Score", f"{(best_window.get('score') or 0):.2f}"),
                ("Start", _format_timestamp(best_window.get("start"))),
                ("End", _format_timestamp(best_window.get("end"))),
            ]
        )

        render_section_heading("Upcoming Event")
        if events:
            event = events[0]
            st.markdown(f"### {event.get('name', 'Upcoming event')}")
            st.write(event.get("description") or "A celestial event is available for tonight.")
            st.caption(f"Category: {event.get('category', 'General')} | Type: {event.get('event_type', 'General')}")
        else:
            st.info("Upcoming event information is temporarily unavailable.")

        st.markdown("---")
        st.subheader("Quick Actions")
        action_columns = st.columns(3)
        action_columns[0].button("Plan Tonight")
        action_columns[1].button("Learn about the Moon")
        action_columns[2].button("Learn about Mars")
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
