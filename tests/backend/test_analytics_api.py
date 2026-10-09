"""API tests for the Analytics endpoint."""

from __future__ import annotations

from datetime import datetime, timezone


def test_analytics_endpoint_returns_valid_payload(client) -> None:
    """Verify GET /api/analytics returns 200 with summary metrics and trajectory data."""
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    response = client.get(
        "/api/analytics",
        params={
            "latitude": 18.5204,
            "longitude": 73.8567,
            "timestamp": now.isoformat(),
        },
    )

    assert response.status_code == 200
    payload = response.json()

    assert "target_scores" in payload
    assert "category_distribution" in payload
    assert "elevation_trajectories" in payload
    assert "telemetry" in payload
