"""Skyfield adapter placeholder.

This adapter encapsulates Skyfield dependencies and exposes a stable interface
for the astronomy engine. The rest of the project should depend on adapter
interfaces or service interfaces instead of Skyfield types.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from astronomy_engine.core.domain import ObservationContext


class SkyfieldAdapter(ABC):
    """Abstract adapter interface for Skyfield data access."""

    @abstractmethod
    def initialize(self) -> None:
        """Load ephemeris data and prepare the Skyfield runtime."""
        raise NotImplementedError

    @abstractmethod
    def get_planet_state(self, planet_name: str, context: ObservationContext) -> object:
        """Return raw skyfield state data for a named planet."""
        raise NotImplementedError

    @abstractmethod
    def get_moon_state(self, context: ObservationContext) -> object:
        """Return raw skyfield state data for the Moon."""
        raise NotImplementedError

    @abstractmethod
    def get_sun_state(self, context: ObservationContext) -> object:
        """Return raw skyfield state data for the Sun."""
        raise NotImplementedError

    @abstractmethod
    def get_rise_set(self, body_name: str, context: ObservationContext) -> object:
        """Return raw rise/set state data for a celestial body."""
        raise NotImplementedError
