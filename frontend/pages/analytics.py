"""Analytics Dashboard page for the Streamlit frontend.

Provides deep-space observation analytics, category distributions, target suitability
scores, and 24-hour planetary elevation trajectories.
"""

from __future__ import annotations

from datetime import datetime, timezone
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from frontend.client import ApiClient, FrontendApiError
from frontend.ui import (
    inject_astronomy_styles,
    render_error,
    render_location_selector,
    render_metrics,
    render_section_heading,
    render_time_selector,
)


def render() -> None:
    """Render the Analytics Dashboard page."""
    inject_astronomy_styles(is_landing=False)

    st.title("📊 Observation Analytics & Intelligence")
    st.caption("Real-time telemetry, target suitability scores, category breakdowns, and 24-hour planetary trajectories.")

    col_loc, col_time = st.columns([1, 1])
    with col_loc:
        latitude, longitude, location_label = render_location_selector()
    with col_time:
        timestamp = render_time_selector()

    client = ApiClient()

    try:
        data = client.get_analytics(
            latitude=latitude,
            longitude=longitude,
            timestamp=timestamp,
            elevation=0.0,
        )
    except FrontendApiError as exc:
        render_error(f"Unable to load analytics data: {exc}")
        return

    telemetry = data.get("telemetry", {})
    scores = data.get("target_scores", [])
    categories = data.get("category_distribution", {})
    trajectories = data.get("elevation_trajectories", [])

    # 1. Telemetry Metric Cards
    render_metrics([
        ("Location", location_label),
        ("Dark Sky Window", f"{telemetry.get('dark_hours', 8.0):.1f} Hours"),
        ("Visible Targets", f"{telemetry.get('visible_target_count', 0)} Bodies"),
        ("APOD Archive", f"{telemetry.get('total_apod_entries', 30)} Photos"),
    ])

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Charts Row 1: Target Suitability Scores & Category Breakdown
    col_chart1, col_chart2 = st.columns([1.5, 1])

    with col_chart1:
        render_section_heading("Target Suitability Scores", "Ranked observing score (0-100) based on altitude and visibility.")
        if scores:
            df_scores = pd.DataFrame(scores)
            fig_bar = px.bar(
                df_scores,
                x="score",
                y="object_name",
                orientation="h",
                color="score",
                color_continuous_scale=["#1e293b", "#0284c7", "#38bdf8", "#38bdf8"],
                text="score",
                labels={"score": "Viewing Score (0-100)", "object_name": "Target Object"},
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f8fafc", "family": "Inter, sans-serif"},
                coloraxis_showscale=False,
                margin=dict(l=10, r=20, t=10, b=10),
                height=320,
                yaxis=dict(autorange="reversed"),
            )
            fig_bar.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No target suitability metrics available for this location.")

    with col_chart2:
        render_section_heading("Category Distribution", "Breakdown of observable targets by astronomical type.")
        if categories:
            df_cat = pd.DataFrame([
                {"Category": cat, "Count": count} for cat, count in categories.items() if count > 0
            ])
            fig_donut = px.pie(
                df_cat,
                names="Category",
                values="Count",
                hole=0.55,
                color_discrete_sequence=["#38bdf8", "#818cf8", "#34d399", "#f43f5e"],
            )
            fig_donut.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font={"color": "#f8fafc", "family": "Inter, sans-serif"},
                legend=dict(orientation="h", y=-0.1),
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No category breakdown data available.")

    st.divider()

    # 3. 24-Hour Planetary Elevation Trajectories
    render_section_heading("24-Hour Elevation Trajectories", "Altitude vs hour (00:00 - 23:00) for major celestial targets above local horizon.")

    if trajectories:
        fig_traj = go.Figure()
        colors = ["#38bdf8", "#f43f5e", "#fbbf24", "#a855f7", "#34d399"]

        for idx, traj in enumerate(trajectories):
            body_name = traj.get("object_name", "")
            pts = traj.get("points", [])
            hours = [p["hour"] for p in pts]
            alts = [p["altitude"] for p in pts]

            fig_traj.add_trace(
                go.Scatter(
                    x=hours,
                    y=alts,
                    mode="lines+markers",
                    name=body_name,
                    line=dict(width=2.5, color=colors[idx % len(colors)]),
                    marker=dict(size=5),
                )
            )

        # Add Horizon Line (Altitude = 0°)
        fig_traj.add_shape(
            type="line",
            x0=0,
            x1=1,
            xref="paper",
            y0=0,
            y1=0,
            line=dict(color="#94a3b8", width=1.5, dash="dash"),
        )
        fig_traj.add_annotation(
            x=0.01,
            y=2,
            xref="paper",
            text="Local Horizon (0° Altitude)",
            showarrow=False,
            font=dict(color="#94a3b8", size=11),
        )

        fig_traj.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            font={"color": "#f8fafc", "family": "Inter, sans-serif"},
            xaxis=dict(title="Hour of Day (UTC)", gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(title="Altitude Angle (°)", gridcolor="rgba(255,255,255,0.05)", range=[-90, 90]),
            legend=dict(orientation="h", y=1.12),
            margin=dict(l=20, r=20, t=30, b=20),
            height=400,
        )
        st.plotly_chart(fig_traj, use_container_width=True)

    st.divider()

    # 4. Target Details Table
    render_section_heading("Observation Target Data Summary", "Detailed altitude, visibility state, and suitability ratings.")
    if scores:
        df_table = pd.DataFrame(scores)
        df_table.columns = ["Target Object", "Suitability Score", "Current Altitude (°)", "Visible Now", "Category"]
        df_table["Visible Now"] = df_table["Visible Now"].apply(lambda v: "✅ Visible" if v else "❌ Below Horizon")
        st.dataframe(df_table, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render()
