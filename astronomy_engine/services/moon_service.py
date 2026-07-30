"""Abstract Moon service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from astronomy_engine.core.domain import MoonPhase, MoonVisibility, ObservationContext


class MoonService(ABC):
    """Public Moon service interface for astronomy calculations."""

    @abstractmethod
    def get_moon_phase(self, context: ObservationContext) -> MoonPhase:
        """Return the moon phase and illumination for the requested context."""
        raise NotImplementedError

    @abstractmethod
    def get_lunar_visibility(self, context: ObservationContext) -> MoonVisibility:
        """Return lunar rise/set and visibility details for the requested context."""
        raise NotImplementedError
