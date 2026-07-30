"""Abstract Sun service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from astronomy_engine.core.domain import ObservationContext, SolarState


class SunService(ABC):
    """Public Sun service interface for solar astronomy."""

    @abstractmethod
    def get_solar_state(self, context: ObservationContext) -> SolarState:
        """Return sunrise, sunset, and solar state for the requested context."""
        raise NotImplementedError

    @abstractmethod
    def get_sunrise_sunset(self, context: ObservationContext) -> SolarState:
        """Return day boundary times for the requested context."""
        raise NotImplementedError
