"""API tests for the Events endpoint."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from database.models import CelestialEvent, Planet


def test_events_endpoint_returns_upcoming_events(client, db_session) -> None:
    now = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc)
    planet = Planet(
        name="mars",
        display_name="Mars",
        category="terrestrial",
        description="The red planet.",
    )
    db_session.add(planet)
    db_session.commit()

    db_session.add_all(
        [
            CelestialEvent(
                event_type="conjunction",
                title="Past Mars Conjunction",
                description="Already occurred.",
                starts_at=now - timedelta(days=2),
                planet_id=planet.id,
            ),
            CelestialEvent(
                event_type="opposition",
                title="Mars Opposition",
                description="Mars reaches opposition.",
                starts_at=now + timedelta(days=3),
                ends_at=now + timedelta(days=4),
                planet_id=planet.id,
            ),
        ]
    )
    db_session.commit()

    response = client.get(
        "/api/events",
        params={
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timestamp": now.isoformat(),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert payload[0]["name"] == "Mars Opposition"
    assert payload[0]["event_type"] == "opposition"
    assert payload[0]["visible_objects"] == ["Mars"]


def test_events_endpoint_returns_empty_list_when_no_upcoming_events(client, db_session) -> None:
    now = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc)
    db_session.add(
        CelestialEvent(
            event_type="conjunction",
            title="Past Event",
            description="Already occurred.",
            starts_at=now - timedelta(days=1),
        )
    )
    db_session.commit()

    response = client.get(
        "/api/events",
        params={
            "latitude": 0.0,
            "longitude": 0.0,
            "timestamp": now.isoformat(),
        },
    )

    assert response.status_code == 200
    assert response.json() == []
