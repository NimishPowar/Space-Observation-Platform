"""Explore page for the Streamlit frontend."""

from __future__ import annotations

import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import (
    inject_astronomy_styles,
    render_error,
    render_loading_state,
    render_location_selector,
    render_metrics,
    render_night_sky_map,
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
    inject_astronomy_styles()

    st.markdown("### ✨ Explore the Night Sky")
    st.caption("Real-time interactive sky map, visible planets, bright stars, and constellation guide.")

    col_loc, col_time = st.columns([1, 1])
    with col_loc:
        latitude, longitude, location_label = render_location_selector()
    with col_time:
        timestamp = render_time_selector()

    elevation = 0.0

    client = ApiClient()
    try:
        moon = sun = planets = stars = constellations = visibility = events = None

        def load_data() -> None:
            nonlocal moon, sun, planets, stars, constellations, visibility, events
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
            try:
                stars = client.get_stars(
                    latitude=latitude,
                    longitude=longitude,
                    timestamp=timestamp,
                    elevation=elevation,
                    min_altitude=-10.0,
                )
            except FrontendApiError:
                stars = []

            try:
                constellations = client.get_constellations(
                    latitude=latitude,
                    longitude=longitude,
                    timestamp=timestamp,
                    elevation=elevation,
                )
            except FrontendApiError:
                constellations = []

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
        render_status(f"📍 Location: **{location_label}** | Lat: `{latitude:.2f}°`, Lon: `{longitude:.2f}°`", kind="info")

        # Top Overview Cards
        render_section_heading("Sky Conditions & Solar Overview")
        render_metrics(
            [
                ("Moon Phase", moon.get("phase_name", "N/A")),
                ("Illumination", f"{(moon.get('illumination') or 0):.1%}"),
                ("Sunrise (UTC)", _format_timestamp(sun.get("sunrise"))),
                ("Sunset (UTC)", _format_timestamp(sun.get("sunset"))),
            ]
        )

        st.markdown("---")

        # Interactive Night Sky Map View
        render_section_heading("🌌 Interactive Night Sky Map")

        col_map, col_ctrl = st.columns([3, 1])

        with col_ctrl:
            st.markdown("#### Sky Map Controls")
            toggle_constellations = st.checkbox("Show Constellation Lines", value=True)
            toggle_stars = st.checkbox("Show Visible Stars", value=True)
            toggle_planets = st.checkbox("Show Visible Planets", value=True)
            max_mag = st.slider("Max Star Magnitude (Brightness filter)", min_value=0.0, max_value=4.0, value=3.0, step=0.5)

        with col_map:
            render_night_sky_map(
                planets=planets or [],
                stars=stars or [],
                constellations=constellations or [],
                moon=moon,
                sun=sun,
                show_constellations=toggle_constellations,
                show_stars=toggle_stars,
                show_planets=toggle_planets,
                max_magnitude=max_mag,
            )

        st.markdown("---")

        # Detailed Data Tabs
        tab_planets, tab_stars, tab_const, tab_visibility = st.tabs(
            ["🪐 Visible Planets", "⭐ Visible Stars", "✨ Constellation Guide", "🔭 Visibility Summary"]
        )

        with tab_planets:
            st.markdown("### Visible Planets")
            planet_rows = [
                {
                    "Object": item.get("object_name", "N/A"),
                    "Altitude (°)": item.get("altitude"),
                    "Azimuth (°)": item.get("azimuth"),
                    "Magnitude": item.get("magnitude"),
                    "RA (°)": item.get("right_ascension"),
                    "Dec (°)": item.get("declination"),
                    "Visible": "YES" if item.get("is_visible") else "NO",
                }
                for item in planets or []
            ]
            render_table(planet_rows)

        with tab_stars:
            st.markdown("### Bright Stars Catalog")
            visible_stars_list = [s for s in (stars or []) if s.get("is_visible")]
            star_rows = [
                {
                    "Star": item.get("name", "N/A"),
                    "Bayer": item.get("bayer_designation", "N/A"),
                    "Constellation": item.get("constellation", "N/A"),
                    "Altitude (°)": item.get("altitude"),
                    "Azimuth (°)": item.get("azimuth"),
                    "Mag": item.get("magnitude"),
                    "Spectral Class": item.get("spectral_type"),
                }
                for item in visible_stars_list
            ]
            render_table(star_rows)

        with tab_const:
            st.markdown("### Visible Constellations")
            const_rows = [
                {
                    "Constellation": item.get("name"),
                    "Latin Name": item.get("latin_name"),
                    "Abbr": item.get("abbreviation"),
                    "Center Alt (°)": item.get("center_altitude"),
                    "Center Az (°)": item.get("center_azimuth"),
                    "Visible": "YES" if item.get("is_visible") else "NO",
                }
                for item in (constellations or [])
            ]
            render_table(const_rows)

        with tab_visibility:
            st.markdown("### Best Viewing Windows")
            best_window = (visibility or [{}])[0]
            render_metrics(
                [
                    ("Best Object", best_window.get("object_name", "N/A")),
                    ("Score", f"{(best_window.get('score') or 0):.2f}"),
                    ("Start", _format_timestamp(best_window.get("start"))),
                    ("End", _format_timestamp(best_window.get("end"))),
                ]
            )

        st.markdown("---")
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
        action_columns[1].button("Discover Moon")
        action_columns[2].button("Discover Mars")
    except FrontendApiError as exc:
        render_error(str(exc))


if __name__ == "__main__":
    render()
