"""Backend use cases for astronomy engine operations."""

from __future__ import annotations

from astronomy_engine.core.domain import ObservationContext
from astronomy_engine.core.engine import AstronomyEngine
from astronomy_engine.core.domain import MoonPhase, PlanetPosition, SolarState, VisibilityWindow


class AstronomyUseCase:
    """Use case layer that delegates astronomy queries to the engine."""

    def __init__(self, engine: AstronomyEngine) -> None:
        self._engine = engine

    def get_moon_summary(self, context: ObservationContext) -> MoonPhase:
        """Return a moon phase summary for the given context."""
        return self._engine.get_moon_summary(context)

    def get_planetary_positions(self, context: ObservationContext) -> list[PlanetPosition]:
        """Return visible planetary positions for the given context."""
        return self._engine.get_planetary_positions(context)

    def get_solar_summary(self, context: ObservationContext) -> SolarState:
        """Return solar state for the given context."""
        return self._engine.get_solar_summary(context)

    def get_visibility_windows(
        self,
        context: ObservationContext,
        object_names: list[str] | None = None,
    ) -> list[VisibilityWindow]:
        """Return visibility windows for a set of requested objects."""
        return self._engine.get_visibility_windows(context, object_names)
