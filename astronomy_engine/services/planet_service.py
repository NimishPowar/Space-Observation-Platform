"""Abstract Planet service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from astronomy_engine.core.domain import ObservationContext, PlanetPosition


class PlanetService(ABC):
    """Public Planet service interface for planetary astronomy."""

    @abstractmethod
    def list_visible_planets(self, context: ObservationContext) -> List[PlanetPosition]:
        """Return all visible planet positions for the specified context."""
        raise NotImplementedError

    @abstractmethod
    def get_planet_position(
        self,
        name: str,
        context: ObservationContext,
    ) -> PlanetPosition:
        """Return a single planet position by name for the specified context."""
        raise NotImplementedError
