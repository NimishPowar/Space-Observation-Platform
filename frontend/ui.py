"""Common Streamlit UI helpers for the frontend application."""

from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Callable, Dict, List, Optional

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def inject_astronomy_styles() -> None:
    """Inject custom CSS for futuristic deep space glassmorphic aesthetics and top navigation bar."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Core Page & Background */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e1b4b 0%, #090d16 50%, #030712 100%) !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4, .main-title {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -0.025em !important;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h1 {
        font-size: 2.3rem !important;
        margin-bottom: 0.2rem !important;
    }

    h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
    }

    /* Top Navbar Radio Group Styling */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        display: flex !important;
        flex-direction: row !important;
        justify-content: flex-end !important;
        align-items: center !important;
        gap: 10px !important;
        background: rgba(15, 23, 42, 0.75) !important;
        padding: 6px 10px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] label {
        background: transparent !important;
        padding: 8px 22px !important;
        border-radius: 10px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.98rem !important;
        color: #94a3b8 !important;
        cursor: pointer !important;
        transition: all 0.25s ease-in-out !important;
        border: 1px solid transparent !important;
        margin: 0 !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] label:hover {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.12) !important;
        border-color: rgba(56, 189, 248, 0.2) !important;
    }

    div[data-testid="stRadio"] > div[role="radiogroup"] label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] div[aria-checked="true"] {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        color: #ffffff !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        box-shadow: 0 0 16px rgba(56, 189, 248, 0.45) !important;
    }

    /* Hide standard radio dot indicator */
    div[data-testid="stRadio"] > div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }

    /* Glassmorphic Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(56, 189, 248, 0.18) !important;
        border-radius: 14px !important;
        padding: 16px 20px !important;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 0 0 rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4) !important;
    }

    div[data-testid="stMetric"] label {
        color: #94a3b8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 20px rgba(56, 189, 248, 0.3) !important;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        color: #94a3b8 !important;
        background: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 22px !important;
        transition: all 0.2s ease !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.08) !important;
    }

    button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 3px solid #38bdf8 !important;
        background: rgba(56, 189, 248, 0.12) !important;
    }

    /* Custom Input Fields */
    input[type="text"], div[data-baseweb="select"] > div {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Custom Buttons */
    div.stButton > button {
        border-radius: 10px !important;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 14px 0 rgba(0, 0, 0, 0.3) !important;
    }

    div.stButton > button:hover {
        border-color: #38bdf8 !important;
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.5) !important;
        color: #ffffff !important;
        transform: translateY(-1px);
    }

    /* Info / Warning / Success Alerts */
    div.stAlert {
        border-radius: 12px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Code & Telemetry */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_section_heading(title: str, caption: Optional[str] = None) -> None:
    """Render a styled heading for a page section with optional caption."""
    st.markdown(f"### {title}")
    if caption:
        st.caption(caption)


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
    with st.spinner("✨ Fetching astronomical data..."):
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
    """Render a location selector widget and persist coordinates in session state."""
    from frontend.client import ApiClient, FrontendApiError

    city_query = st.session_state.get("location_query", "Mumbai")
    location_label = st.session_state.get("location_label", "Mumbai")
    latitude = float(st.session_state.get("location_latitude", 19.0760))
    longitude = float(st.session_state.get("location_longitude", 72.8777))

    col1, col2 = st.columns([3, 1])
    with col1:
        new_query = st.text_input("🔍 Observer Location City", value=city_query, key="location_query_top")
    with col2:
        st.write("")
        st.write("")
        if st.button("Set Location", use_container_width=True):
            try:
                client = ApiClient()
                match = client.search_city(new_query)[0]
                latitude = float(match["lat"])
                longitude = float(match["lon"])
                location_label = match.get("display_name", new_query)
                st.session_state["location_latitude"] = latitude
                st.session_state["location_longitude"] = longitude
                st.session_state["location_label"] = location_label
                st.session_state["location_query"] = new_query
                st.success(f"Location set to {location_label}.")
            except FrontendApiError as exc:
                st.error(str(exc))

    st.caption(f"📍 **Current Observation Coordinates**: {location_label} (`{latitude:.2f}° N, {longitude:.2f}° E`)")
    return latitude, longitude, location_label


def render_time_selector() -> str | None:
    """Render a friendly time selection widget and return an ISO 8601 string."""
    when_mode = st.radio("⏰ Observation Timestamp", ["Right Now", "Tonight", "Pick Date & Time"], horizontal=True)

    if when_mode == "Right Now":
        return datetime.now(timezone.utc).isoformat()

    if when_mode == "Tonight":
        tonight = datetime.now(timezone.utc).replace(hour=20, minute=30, second=0, microsecond=0)
        if tonight < datetime.now(timezone.utc):
            tonight += timedelta(days=1)
        return tonight.isoformat()

    col1, col2 = st.columns(2)
    with col1:
        selected_date = st.date_input("Date", value=date.today())
    with col2:
        selected_time = st.time_input("Time", value=time(20, 30))
    selected_dt = datetime.combine(selected_date, selected_time, tzinfo=timezone.utc)
    return selected_dt.isoformat()


def render_night_sky_map(
    planets: list[dict],
    stars: list[dict],
    constellations: list[dict],
    moon: dict | None = None,
    sun: dict | None = None,
    show_constellations: bool = True,
    show_stars: bool = True,
    show_planets: bool = True,
    max_magnitude: float = 3.5,
) -> None:
    """Render an interactive 2D Polar Stereographic Night Sky Map using Plotly."""
    fig = go.Figure()

    # 1. Constellation Lines
    if show_constellations and constellations:
        star_lookup = {s["name"]: s for s in stars if s.get("name")}
        for const in constellations:
            lines = const.get("lines") or []
            for pair in lines:
                if len(pair) == 2 and pair[0] in star_lookup and pair[1] in star_lookup:
                    s1 = star_lookup[pair[0]]
                    s2 = star_lookup[pair[1]]
                    alt1, az1 = s1.get("altitude"), s1.get("azimuth")
                    alt2, az2 = s2.get("altitude"), s2.get("azimuth")

                    if alt1 is not None and alt2 is not None and (alt1 >= -5.0 or alt2 >= -5.0):
                        r1 = max(0, 90.0 - alt1)
                        r2 = max(0, 90.0 - alt2)
                        fig.add_trace(
                            go.Scatterpolar(
                                r=[r1, r2],
                                theta=[az1, az2],
                                mode="lines",
                                line=dict(color="rgba(56, 189, 248, 0.45)", width=1.5, dash="dot"),
                                hoverinfo="skip",
                                showlegend=False,
                            )
                        )

    # 2. Bright Stars
    if show_stars and stars:
        visible_stars = [s for s in stars if (s.get("altitude") or -90) >= 0.0 and (s.get("magnitude") or 99) <= max_magnitude]
        if visible_stars:
            r_stars = [max(0, 90.0 - s["altitude"]) for s in visible_stars]
            theta_stars = [s["azimuth"] for s in visible_stars]
            sizes = [max(4, min(18, 16.0 - 3.5 * float(s.get("magnitude", 1.0)))) for s in visible_stars]
            colors = [s.get("color_hex", "#ffffff") for s in visible_stars]
            hover_text = [
                f"<b>{s.get('name')}</b> ({s.get('bayer_designation')})<br>"
                f"Constellation: {s.get('constellation')}<br>"
                f"Mag: {s.get('magnitude')}<br>"
                f"Alt: {s.get('altitude')}° | Az: {s.get('azimuth')}°"
                for s in visible_stars
            ]

            fig.add_trace(
                go.Scatterpolar(
                    r=r_stars,
                    theta=theta_stars,
                    mode="markers",
                    marker=dict(
                        size=sizes,
                        color=colors,
                        opacity=0.95,
                        line=dict(color="rgba(255, 255, 255, 0.6)", width=1),
                    ),
                    text=hover_text,
                    hoverinfo="text",
                    name="Stars",
                )
            )

    # 3. Planets
    if show_planets and planets:
        planet_colors = {
            "Mercury": "#a0a0a0",
            "Venus": "#fef08a",
            "Mars": "#ef4444",
            "Jupiter": "#fbbf24",
            "Saturn": "#eab308",
            "Uranus": "#38bdf8",
            "Neptune": "#3b82f6",
        }
        visible_planets = [p for p in planets if (p.get("altitude") or -90) >= 0.0]
        if visible_planets:
            r_planets = [max(0, 90.0 - p["altitude"]) for p in visible_planets]
            theta_planets = [p["azimuth"] for p in visible_planets]
            p_names = [p.get("object_name", "Planet") for p in visible_planets]
            p_colors = [planet_colors.get(name, "#38bdf8") for name in p_names]
            p_text = [
                f"<b>{p.get('object_name')}</b> (Planet)<br>"
                f"Alt: {p.get('altitude')}° | Az: {p.get('azimuth')}°<br>"
                f"Mag: {p.get('magnitude', 'N/A')}"
                for p in visible_planets
            ]

            fig.add_trace(
                go.Scatterpolar(
                    r=r_planets,
                    theta=theta_planets,
                    mode="markers+text",
                    marker=dict(
                        size=15,
                        color=p_colors,
                        symbol="circle",
                        line=dict(color="#ffffff", width=2),
                    ),
                    text=p_names,
                    textposition="top center",
                    textfont=dict(color="#f8fafc", size=12, family="Space Grotesk"),
                    hovertext=p_text,
                    hoverinfo="text",
                    name="Planets",
                )
            )

    # Layout configuration
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 90],
                tickvals=[0, 30, 60, 90],
                ticktext=["Zenith (90°)", "60°", "30°", "Horizon (0°)"],
                color="#64748b",
                gridcolor="rgba(56, 189, 248, 0.12)",
                showline=False,
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90,  # 0 deg (North) at top
                tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                ticktext=["<b>N</b>", "NE", "<b>E</b>", "SE", "<b>S</b>", "SW", "<b>W</b>", "NW"],
                color="#38bdf8",
                gridcolor="rgba(56, 189, 248, 0.12)",
                linecolor="rgba(56, 189, 248, 0.25)",
            ),
            bgcolor="#050811",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(color="#94a3b8", family="Space Grotesk"),
        ),
        margin=dict(l=40, r=40, t=40, b=60),
        height=580,
    )

    st.plotly_chart(fig, use_container_width=True)
