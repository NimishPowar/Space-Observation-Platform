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
    def get_body_state(self, body_name: str, context: ObservationContext) -> object:
        """Return raw Skyfield state data for a named celestial body."""
        raise NotImplementedError

    @abstractmethod
    def get_solar_state(self, context: ObservationContext) -> object:
        """Return raw Solar state data for the requested context."""
        raise NotImplementedError
