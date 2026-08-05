"""Backend use cases for astronomy engine operations."""

from __future__ import annotations

from typing import List, Optional

from astronomy_engine.core.domain import (
    ConstellationData,
    MoonPhase,
    ObservationContext,
    PlanetPosition,
    SkyMapData,
    SolarState,
    StarPosition,
    VisibilityWindow,
)
from astronomy_engine.core.engine import AstronomyEngine


class AstronomyUseCase:
    """Use case layer that delegates astronomy queries to the engine."""

    def __init__(self, engine: AstronomyEngine) -> None:
        self._engine = engine

    def get_moon_summary(self, context: ObservationContext) -> MoonPhase:
        """Return a moon phase summary for the given context."""
        return self._engine.get_moon_summary(context)

    def get_planetary_positions(self, context: ObservationContext) -> List[PlanetPosition]:
        """Return visible planetary positions for the given context."""
        return self._engine.get_planetary_positions(context)

    def get_solar_summary(self, context: ObservationContext) -> SolarState:
        """Return solar state for the given context."""
        return self._engine.get_solar_summary(context)

    def get_visibility_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        """Return visibility windows for a set of requested objects."""
        return self._engine.get_visibility_windows(context, object_names)

    def get_star_positions(
        self,
        context: ObservationContext,
        min_altitude: float = 0.0,
    ) -> List[StarPosition]:
        """Return visible star positions for the given context."""
        return self._engine.get_star_positions(context, min_altitude=min_altitude)

    def get_constellations(
        self,
        context: ObservationContext,
    ) -> List[ConstellationData]:
        """Return visible constellations for the given context."""
        return self._engine.get_constellations(context)

    def get_skymap_data(
        self,
        context: ObservationContext,
    ) -> SkyMapData:
        """Return aggregated sky map data for the given context."""
        return self._engine.get_skymap_data(context)
