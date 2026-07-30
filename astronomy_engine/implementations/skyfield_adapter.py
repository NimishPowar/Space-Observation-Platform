"""Stub Skyfield adapter implementation.

This adapter encapsulates the Skyfield contract without relying on any actual
Skyfield runtime. It provides a placeholder implementation for engine wiring
and service integration.
"""

from __future__ import annotations

from astronomy_engine.adapters.skyfield_adapter import SkyfieldAdapter
from astronomy_engine.core.domain import ObservationContext


class StubSkyfieldAdapter(SkyfieldAdapter):
    """Placeholder Skyfield adapter that returns no-op state objects."""

    def initialize(self) -> None:
        """Prepare the adapter runtime."""
        return None

    def get_planet_state(self, planet_name: str, context: ObservationContext) -> dict:
        """Return placeholder state for a named planet."""
        return {"planet_name": planet_name}

    def get_moon_state(self, context: ObservationContext) -> dict:
        """Return placeholder state for the Moon."""
        return {"body_name": "Moon"}

    def get_sun_state(self, context: ObservationContext) -> dict:
        """Return placeholder state for the Sun."""
        return {"body_name": "Sun"}

    def get_rise_set(self, body_name: str, context: ObservationContext) -> dict:
        """Return placeholder rise/set state for a celestial body."""
        return {"body_name": body_name}
