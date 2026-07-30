"""Core astronomy engine orchestration."""

from __future__ import annotations

from astronomy_engine.core.domain import ObservationContext, MoonPhase, PlanetPosition, SolarState, VisibilityWindow
from astronomy_engine.services import MoonService, PlanetService, SunService, VisibilityService


class AstronomyEngine:
    """Orchestrator for astronomy engine services."""

    def __init__(
        self,
        moon_service: MoonService,
        planet_service: PlanetService,
        sun_service: SunService,
        visibility_service: VisibilityService,
    ) -> None:
        self._moon_service = moon_service
        self._planet_service = planet_service
        self._sun_service = sun_service
        self._visibility_service = visibility_service

    def get_moon_summary(self, context: ObservationContext) -> MoonPhase:
        """Return moon phase and visibility details for the given context."""
        return self._moon_service.get_moon_phase(context)

    def get_planetary_positions(
        self,
        context: ObservationContext,
    ) -> list[PlanetPosition]:
        """Return visible planet positions for the given context."""
        return self._planet_service.list_visible_planets(context)

    def get_solar_summary(self, context: ObservationContext) -> SolarState:
        """Return solar state data for the given context."""
        return self._sun_service.get_solar_state(context)

    def get_visibility_windows(
        self,
        context: ObservationContext,
        object_names: list[str] | None = None,
    ) -> list[VisibilityWindow]:
        """Return visibility windows for requested objects and context."""
        return self._visibility_service.compute_visibility(context, object_names)

    def get_best_observation_windows(
        self,
        context: ObservationContext,
        object_names: list[str] | None = None,
    ) -> list[VisibilityWindow]:
        """Return prioritized observation windows for the requested context."""
        return self._visibility_service.compute_best_observation_windows(
            context,
            object_names,
        )
