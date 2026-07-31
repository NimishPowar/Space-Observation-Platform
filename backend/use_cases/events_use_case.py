"""Use cases for celestial event reference data served from the database."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from database.models import CelestialEvent
from database.repository import CelestialEventRepository


@dataclass(frozen=True)
class CelestialEventResult:
    """Database-backed celestial event summary for API responses."""

    event_id: str
    name: str
    category: str
    event_type: str
    description: str | None
    start_time: datetime
    end_time: datetime | None
    visible_objects: list[str] | None
    magnitude: float | None
    location: dict | None


class EventsUseCase:
    """Retrieve upcoming celestial events from persisted reference data."""

    def __init__(self, event_repository: CelestialEventRepository) -> None:
        self._event_repository = event_repository

    def list_upcoming_events(
        self,
        from_time: datetime,
        limit: int = 50,
    ) -> list[CelestialEventResult]:
        """Return upcoming events ordered by start time."""
        events = self._event_repository.list_upcoming(from_time=from_time, limit=limit)
        return [self._to_result(event) for event in events]

    @staticmethod
    def _to_result(event: CelestialEvent) -> CelestialEventResult:
        visible_objects = None
        category = event.event_type

        if event.planet is not None:
            visible_objects = [event.planet.display_name]
            category = event.planet.category

        return CelestialEventResult(
            event_id=str(event.id),
            name=event.title,
            category=category,
            event_type=event.event_type,
            description=event.description,
            start_time=event.starts_at,
            end_time=event.ends_at,
            visible_objects=visible_objects,
            magnitude=None,
            location=None,
        )
