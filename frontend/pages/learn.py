"""Discovery & Interactive Learning page for the Streamlit frontend."""

from __future__ import annotations

from datetime import date, datetime
import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import render_error, render_section_heading


def render_astronomy_basics(client: ApiClient) -> None:
    """Render Module 1: Astronomy Basics."""
    try:
        categories = client.get_discovery_categories()
    except FrontendApiError:
        categories = []

    cat_options = ["All Categories"] + [c["name"] for c in categories]
    cat_slug_map = {c["name"]: c["slug"] for c in categories}

    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("🔍 Search Astronomy Topics", placeholder="e.g. Black Holes, Comets, Nebulae...")
    with col2:
        selected_cat_name = st.selectbox("Filter Category", cat_options)

    selected_cat_slug = cat_slug_map.get(selected_cat_name) if selected_cat_name != "All Categories" else None

    try:
        topics = client.get_discovery_topics(query=search_query if search_query else None, category=selected_cat_slug)
    except FrontendApiError as exc:
        render_error(str(exc))
        topics = []

    if not topics:
        st.warning("No matching astronomy topics found. Try adjusting your search query.")
        return

    topic_titles = [t["title"] for t in topics]
    selected_title = st.selectbox("Select Topic to Read", topic_titles)
    selected_topic = next((t for t in topics if t["title"] == selected_title), topics[0])

    render_section_heading(selected_topic["title"])
    st.markdown(f"**Category:** `{selected_topic.get('category_name', 'General')}` | **Slug:** `{selected_topic.get('slug', 'N/A')}`")

    if selected_topic.get("excerpt"):
        st.info(selected_topic["excerpt"])

    if selected_topic.get("body"):
        st.markdown(selected_topic["body"])

    if selected_topic.get("source_url"):
        st.link_button("🌐 Learn More (NASA Science)", selected_topic["source_url"])


def render_moon_simulator(client: ApiClient) -> None:
    """Render Module 2: Interactive Moon Phase Simulator."""
    render_section_heading("Interactive Moon Phase Simulator")
    st.caption("Step through the 29.5-day synodic lunar cycle to observe real-time calculated illumination, lunar age, and major phase dates.")

    col1, col2 = st.columns([1, 1])
    with col1:
        selected_date = st.date_input("Select Base Date", value=date.today())
    with col2:
        day_offset = st.slider("Lunar Cycle Day Offset (-15 to +15 days)", min_value=-15, max_value=15, value=0)

    try:
        sim_data = client.get_discovery_moon_phase(
            timestamp=selected_date.isoformat(),
            day_offset=day_offset,
        )
    except FrontendApiError as exc:
        render_error(str(exc))
        return

    # Visual representation header
    symbol = sim_data.get("unicode_symbol", "🌕")
    phase_name = sim_data.get("phase_name", "Unknown")
    illum_pct = float(sim_data.get("illumination", 0.0)) * 100.0
    age = sim_data.get("age_days", 0.0)

    m_col1, m_col2 = st.columns([1, 3])
    with m_col1:
        st.markdown(f"<h1 style='text-align: center; font-size: 5rem; margin: 0;'>{symbol}</h1>", unsafe_allow_html=True)
    with m_col2:
        st.markdown(f"### {phase_name}")
        st.write(f"**Illumination:** {illum_pct:.1f}%")
        st.progress(min(max(illum_pct / 100.0, 0.0), 1.0))
        st.write(f"**Lunar Age:** {age:.1f} days into cycle | **Phase Angle:** {sim_data.get('phase_angle', 0.0):.1f}°")

    st.divider()

    # Detailed metrics grid
    g1, g2, g3 = st.columns(3)
    with g1:
        st.subheader("Major Phase History")
        prev_name = sim_data.get("prev_phase_name", "N/A")
        prev_date = sim_data.get("prev_phase_date", "N/A")
        st.metric("Previous Major Phase", prev_name, delta=str(prev_date)[:10] if prev_date else None)

    with g2:
        st.subheader("Next Major Phase")
        next_name = sim_data.get("next_phase_name", "N/A")
        next_date = sim_data.get("next_phase_date", "N/A")
        st.metric("Next Major Phase", next_name, delta=str(next_date)[:10] if next_date else None)

    with g3:
        st.subheader("Lunar Visibility")
        rise = str(sim_data.get("rise_time"))[:16] if sim_data.get("rise_time") else "N/A"
        set_t = str(sim_data.get("set_time"))[:16] if sim_data.get("set_time") else "N/A"
        st.write(f"**Moonrise:** {rise}")
        st.write(f"**Moonset:** {set_t}")

    # Summary explanation card
    st.info(
        f"**About {phase_name}:** "
        f"At a phase angle of {sim_data.get('phase_angle', 0.0):.1f}°, the Moon is {illum_pct:.1f}% illuminated. "
        f"The Moon completes one full synodic cycle (New Moon to New Moon) every 29.53 days as seen from Earth."
    )


def render() -> None:
    """Render the discovery learn page with interactive tabs."""
    st.title("Discovery & Interactive Learning")
    st.caption("Explore foundational astronomy topics, calculated phenomena, and celestial catalogs.")

    client = ApiClient()
    tab1, tab2 = st.tabs(["📚 Astronomy Basics", "🌒 Moon Phase Simulator"])

    with tab1:
        render_astronomy_basics(client)

    with tab2:
        render_moon_simulator(client)


if __name__ == "__main__":
    render()
