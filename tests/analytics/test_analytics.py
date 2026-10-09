"""Unit tests for the AnalyticsDashboard engine."""

from __future__ import annotations

from datetime import datetime, timezone
from analytics.dashboard import AnalyticsDashboard


def test_analytics_dashboard_generates_valid_summary() -> None:
    """Verify AnalyticsDashboard generates scores, trajectories, and telemetry."""
    dashboard = AnalyticsDashboard()
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    summary = dashboard.generate_summary(latitude=18.5204, longitude=73.8567, timestamp=now)

    assert "target_scores" in summary
    assert "category_distribution" in summary
    assert "elevation_trajectories" in summary
    assert "telemetry" in summary

    assert len(summary["target_scores"]) > 0
    assert len(summary["elevation_trajectories"]) == 5
    assert summary["telemetry"]["visible_target_count"] >= 0
