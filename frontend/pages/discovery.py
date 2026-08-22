"""Discovery & Interactive Learning page for the Streamlit frontend."""

from __future__ import annotations

from datetime import date
import streamlit as st
import streamlit.components.v1 as components

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import inject_astronomy_styles, render_error, render_section_heading


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


def render_3d_iframe(src_url: str, height: int = 700) -> None:
    """Render an interactive 3D WebGL iframe with full browser fullscreen permissions."""
    html_code = f"""
    <div style="width: 100%; height: {height}px; position: relative;">
        <iframe 
            src="{src_url}" 
            style="width: 100%; height: 100%; border: none; border-radius: 8px;" 
            allow="fullscreen; accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen="true"
            webkitallowfullscreen="true"
            mozallowfullscreen="true">
        </iframe>
    </div>
    """
    components.html(html_code, height=height + 5, scrolling=False)


def render_solar_system_view() -> None:
    """Render 3D Interactive Solar System View."""
    render_section_heading("3D Solar System View")
    st.caption("Drag to orbit, scroll to zoom, and click any planet to inspect its real-time 3D trajectory and properties.")
    st.link_button("⛶ Open 3D Canvas in Full Tab", "http://127.0.0.1:8000/static/solarsystem/")

    render_3d_iframe("http://127.0.0.1:8000/static/solarsystem/", height=700)


def _get_moon_phase_svg_path(illum_pct: float, age_days: float) -> str:
    """Calculate SVG path d-string for exact lunar phase shadow terminator on a 100x100 circle."""
    frac = max(0.0, min(1.0, illum_pct / 100.0))
    is_waxing = (age_days % 29.53) <= 14.765
    rx = abs(50.0 * (1.0 - 2.0 * frac))

    if is_waxing:
        if frac < 0.5:
            return f"M 50 0 A 50 50 0 0 0 50 100 A {rx:.2f} 50 0 0 1 50 0 Z"
        else:
            return f"M 50 0 A 50 50 0 0 0 50 100 A {rx:.2f} 50 0 0 0 50 0 Z"
    else:
        if frac >= 0.5:
            return f"M 50 0 A 50 50 0 0 1 50 100 A {rx:.2f} 50 0 0 1 50 0 Z"
        else:
            return f"M 50 0 A 50 50 0 0 1 50 100 A {rx:.2f} 50 0 0 0 50 0 Z"


def render_moon_simulator(client: ApiClient) -> None:
    """Render 3D Interactive Moon Phase Simulator."""
    render_section_heading("3D Moon Phase Simulator")
    st.caption("Physically-driven 3D directional lighting Earth-Moon model paired with backend-calculated phase statistics.")

    from pathlib import Path
    moonphase_dir = Path(__file__).resolve().parent.parent.parent / "moonphase"
    moonphase_url = "http://127.0.0.1:8000/static/moonphase/" if (moonphase_dir.is_dir() and any(moonphase_dir.iterdir())) else "https://nimishpowar.github.io/MoonPhase/"
    
    st.link_button("⛶ Open 3D Canvas in Full Tab", moonphase_url)
    render_3d_iframe(moonphase_url, height=600)

    st.markdown("<hr style='margin: 28px 0 20px 0; opacity: 0.15;'>", unsafe_allow_html=True)
    st.markdown("### 🌖 Calculated Lunar Phase Metrics")
    st.caption("Step through the 29.53-day synodic lunar cycle to observe real-time calculated illumination, lunar age, and major phase dates.")

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

    phase_name = sim_data.get("phase_name", "Unknown")
    illum_pct = float(sim_data.get("illumination", 0.0)) * 100.0
    age_days = float(sim_data.get("age_days", 0.0))
    phase_angle = float(sim_data.get("phase_angle", 0.0))
    svg_shadow_path = _get_moon_phase_svg_path(illum_pct, age_days)
    moon_img_url = "http://127.0.0.1:8000/static/moonphase/images/moon.jpg"

    # High-resolution Moon Texture Card with mathematically exact dynamic phase shadow overlay
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 28px; background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(56, 189, 248, 0.25); border-radius: 16px; padding: 24px 28px; margin: 16px 0; backdrop-filter: blur(14px); box-shadow: 0 12px 36px rgba(0,0,0,0.5);">
            <div style="position: relative; width: 135px; height: 135px; border-radius: 50%; overflow: hidden; flex-shrink: 0; box-shadow: 0 0 30px rgba(255, 255, 255, 0.25), inset 0 0 15px rgba(0,0,0,0.85); border: 2px solid rgba(255, 255, 255, 0.3); background-color: #050811;">
                <img src="{moon_img_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%; display: block;" alt="Moon Texture" />
                <svg viewBox="0 0 100 100" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">
                    <path d="{svg_shadow_path}" fill="rgba(5, 8, 17, 0.92)" />
                </svg>
            </div>
            <div style="flex-grow: 1;">
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.7rem; font-weight: 700; color: #f8fafc; margin-bottom: 2px;">{phase_name}</div>
                <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; color: #38bdf8; font-weight: 600; margin-bottom: 10px;">
                    Illumination: {illum_pct:.1f}%
                </div>
                <div style="background: rgba(255, 255, 255, 0.12); height: 10px; border-radius: 5px; overflow: hidden; margin-bottom: 12px;">
                    <div style="background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%); width: {min(max(illum_pct, 0.0), 100.0):.1f}%; height: 100%; border-radius: 5px; box-shadow: 0 0 10px rgba(56, 189, 248, 0.6);"></div>
                </div>
                <div style="font-family: 'Inter', sans-serif; font-size: 0.88rem; color: #94a3b8;">
                    <b>Lunar Age:</b> {age_days:.1f} days into synodic cycle &nbsp;|&nbsp; <b>Phase Angle:</b> {phase_angle:.1f}°
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr style='margin: 20px 0; opacity: 0.1;'>", unsafe_allow_html=True)

    # Detailed metrics grid
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("##### ⏪ Previous Major Phase")
        prev_name = sim_data.get("prev_phase_name", "N/A")
        prev_date = sim_data.get("prev_phase_date", "N/A")
        st.metric("Previous Phase", prev_name, delta=str(prev_date)[:10] if prev_date else None)

    with g2:
        st.markdown("##### ⏩ Next Major Phase")
        next_name = sim_data.get("next_phase_name", "N/A")
        next_date = sim_data.get("next_phase_date", "N/A")
        st.metric("Next Phase", next_name, delta=str(next_date)[:10] if next_date else None)

    with g3:
        st.markdown("##### 🌅 Lunar Visibility")
        rise = str(sim_data.get("rise_time"))[:16] if sim_data.get("rise_time") else "N/A"
        set_t = str(sim_data.get("set_time"))[:16] if sim_data.get("set_time") else "N/A"
        st.write(f"**Moonrise:** `{rise}`")
        st.write(f"**Moonset:** `{set_t}`")

    # Summary explanation card
    st.info(
        f"**About {phase_name}:** "
        f"At a phase angle of {phase_angle:.1f}°, the Moon is {illum_pct:.1f}% illuminated. "
        f"The Moon completes one full synodic cycle (New Moon to New Moon) every 29.53 days as seen from Earth."
    )


def render() -> None:
    """Render the discovery page with interactive tabs."""
    inject_astronomy_styles()
    st.title("🌌 Discovery Hub")
    st.caption("Explore foundational astronomy topics, 3D interactive solar system, and physically-driven 3D moon phase simulations.")

    client = ApiClient()
    tab1, tab2, tab3 = st.tabs([
        "📚 Astronomy Basics",
        "🪐 Solar System View",
        "🌒 Moon Phase Simulator",
    ])

    with tab1:
        render_astronomy_basics(client)

    with tab2:
        render_solar_system_view()

    with tab3:
        render_moon_simulator(client)


if __name__ == "__main__":
    render()
