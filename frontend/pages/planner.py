"""Observation planner page for the Streamlit frontend.

Central hub for planning astronomical observations, viewing upcoming celestial events,
and exploring NASA Astronomy Picture of the Day (APOD).
"""

from __future__ import annotations

from datetime import date, datetime
import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import (
    inject_astronomy_styles,
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


def _format_event_category(cat: str) -> str:
    return cat.replace("_", " ").title() if cat else "General"


def _format_iso_date(dt_str: str | None) -> str:
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.strftime("%B %d, %Y at %H:%M UTC")
    except Exception:
        return dt_str.replace("T", " ")


def _build_event_rows(events: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for event in events or []:
        rows.append(
            {
                "Celestial Event": event.get("name", "N/A"),
                "Category": _format_event_category(event.get("category") or event.get("event_type", "")),
                "Event Date & Time": _format_iso_date(event.get("start_time")),
                "Description": event.get("description", "N/A"),
            }
        )
    return rows


def render() -> None:
    """Render the observation planner page with location-aware recommendations, APOD, and events."""
    st.title("🌌 Observation Planner")
    st.caption("Your central hub for planning night sky observations, tracking celestial events, and astronomy insights.")

    tabs = st.tabs(["🎯 Observation Plan", "🖼️ NASA APOD", "📅 Celestial Events"])

    client = ApiClient()

    # Tab 1: Observation Plan
    with tabs[0]:
        col_loc, col_time = st.columns([1, 1])
        with col_loc:
            latitude, longitude, location_label = render_location_selector()
        with col_time:
            timestamp = render_time_selector()
            limit = st.slider("How many recommendations?", min_value=1, max_value=10, value=5)

        if st.button("Plan Observation Session", type="primary"):
            try:
                scores = None

                def load_data() -> None:
                    nonlocal scores
                    scores = client.get_planner(
                        latitude=latitude,
                        longitude=longitude,
                        timestamp=timestamp,
                        elevation=0.0,
                        limit=limit,
                    )

                render_loading_state(load_data)
                render_status(f"Observation plan prepared for {location_label}.", kind="success")
                render_metrics(
                    [
                        ("Location", location_label),
                        ("Recommendations", str(len(scores or []))),
                        ("Top Recommendation", (scores or [{}])[0].get("object_name", "N/A")),
                    ]
                )

                render_section_heading("Best Observation Opportunities")
                for score in scores or []:
                    visibility_window = score.get("visibility_window") or {}
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(
                            f"### {_star_rating(float(score.get('score', 0)))} {score.get('object_name', 'Observation')}"
                        )
                        st.write(score.get("score_reason", "Observation opportunity available."))
                        st.caption(
                            f"⏰ Best Window: {_format_iso_date(visibility_window.get('start'))} → {_format_iso_date(visibility_window.get('end'))}"
                        )
                    with col2:
                        st.metric("Score", f"{float(score.get('score', 0)):.1f}/100")
                    st.divider()

            except FrontendApiError as exc:
                render_error(str(exc))

    # Tab 2: NASA Astronomy Picture of the Day (APOD)
    with tabs[1]:
        st.markdown("### 📷 NASA Astronomy Picture of the Day")
        st.caption("Sourced directly via the platform's backend NASA adapter and ETL storage pipeline.")

        col_apod_hdr, col_apod_date = st.columns([2, 1])
        with col_apod_date:
            selected_apod_date = st.date_input("Browse APOD Date", value=date.today(), key="apod_date_picker")

        try:
            target_date_str = selected_apod_date.isoformat()
            latest = client.get_apod_by_date(target_date_str) if selected_apod_date != date.today() else client.get_apod_today()
            recent_apods = client.get_apod_recent(limit=5)
            if not latest and recent_apods:
                latest = recent_apods[0]

            if latest:
                actual_date = latest.get("apod_date", target_date_str)
                st.subheader(latest.get("title", "NASA Astronomy Picture"))
                if actual_date != target_date_str:
                    st.info(f"ℹ️ Showing closest available APOD record for **{actual_date}** (No APOD entry found for {target_date_str}).")
                st.caption(f"Date: `{actual_date}` | Source: NASA Astronomy Picture of the Day")

                img_url = latest.get("url") or latest.get("hdurl")
                if img_url and latest.get("media_type") == "image":
                    st.image(img_url, use_container_width=True, caption=latest.get("title"))
                elif img_url:
                    st.video(img_url)

                if latest.get("explanation"):
                    with st.expander("📖 Read Explanation", expanded=True):
                        st.write(latest.get("explanation"))

                if latest.get("copyright_text"):
                    st.caption(f"© Copyright: {latest.get('copyright_text')}")

                if recent_apods and len(recent_apods) > 1:
                    render_section_heading("Recent APOD Archive")
                    cols = st.columns(min(4, len(recent_apods) - 1))
                    for idx, apod in enumerate(recent_apods[1:5]):
                        with cols[idx % len(cols)]:
                            apod_img = apod.get("url") or apod.get("hdurl")
                            if apod_img and apod.get("media_type") == "image":
                                st.image(apod_img, caption=f"{apod.get('apod_date')}: {apod.get('title')}", use_container_width=True)
                            else:
                                st.write(f"📅 **{apod.get('apod_date')}**: {apod.get('title')}")
            else:
                st.info("NASA APOD entries will appear here once populated by the ETL pipeline.")
        except FrontendApiError:
            st.info("NASA APOD service is connecting to the backend ETL storage.")

    # Tab 3: Celestial Events
    with tabs[2]:
        st.markdown("### 🌟 Upcoming Celestial Events")
        st.caption("Meteor showers, eclipses, planetary conjunctions, oppositions, equinoxes & solstices.")

        try:
            events = client.get_events(limit=10)
            if events:
                for event in events:
                    with st.container():
                        st.markdown(f"#### 🌠 {event.get('name', 'N/A')}")
                        visible_loc = event.get("visible_from") or "Global"
                        st.caption(
                            f"Category: **{_format_event_category(event.get('category') or event.get('event_type', ''))}** | "
                            f"Starts: **{_format_iso_date(event.get('start_time'))}** | "
                            f"Visible From: 🌍 **{visible_loc}**"
                        )
                        if event.get("description"):
                            st.write(event.get("description"))
                        st.divider()
            else:
                st.info("No upcoming events currently scheduled in the platform catalog.")
        except FrontendApiError as exc:
            st.info("Upcoming event details will load when backend services are active.")


if __name__ == "__main__":
    render()
