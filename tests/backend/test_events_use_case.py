"""Unit tests for EventsUseCase."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from backend.use_cases.events_use_case import EventsUseCase
from database.models import CelestialEvent, Planet
from database.repository import CelestialEventRepository


def test_events_use_case_returns_upcoming_events(db_session) -> None:
    now = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc)
    planet = Planet(
        name="mars",
        display_name="Mars",
        category="terrestrial",
        description="The red planet.",
    )
    db_session.add(planet)
    db_session.commit()

    past_event = CelestialEvent(
        event_type="conjunction",
        title="Past Mars Conjunction",
        description="Already occurred.",
        starts_at=now - timedelta(days=2),
        ends_at=now - timedelta(days=1),
        planet_id=planet.id,
    )
    upcoming_event = CelestialEvent(
        event_type="opposition",
        title="Mars Opposition",
        description="Mars reaches opposition.",
        starts_at=now + timedelta(days=3),
        ends_at=now + timedelta(days=4),
        planet_id=planet.id,
    )
    db_session.add_all([past_event, upcoming_event])
    db_session.commit()

    use_case = EventsUseCase(event_repository=CelestialEventRepository(db_session))
    results = use_case.list_upcoming_events(from_time=now)

    assert len(results) == 1
    assert results[0].name == "Mars Opposition"
    assert results[0].event_type == "opposition"
    assert results[0].category == "terrestrial"
    assert results[0].visible_objects == ["Mars"]


def test_events_use_case_respects_limit(db_session) -> None:
    now = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc)
    for offset in range(5):
        db_session.add(
            CelestialEvent(
                event_type="meteor_shower",
                title=f"Event {offset}",
                description="Upcoming event.",
                starts_at=now + timedelta(days=offset + 1),
            )
        )
    db_session.commit()

    use_case = EventsUseCase(event_repository=CelestialEventRepository(db_session))
    results = use_case.list_upcoming_events(from_time=now, limit=2)

    assert len(results) == 2
    assert results[0].name == "Event 0"
    assert results[1].name == "Event 1"
