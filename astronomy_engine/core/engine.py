"""Core astronomy engine orchestration."""

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
from astronomy_engine.services import (
    ConstellationService,
    DefaultConstellationService,
    DefaultStarService,
    MoonService,
    PlanetService,
    StarService,
    SunService,
    VisibilityService,
)


class AstronomyEngine:
    """Orchestrator for astronomy engine services."""

    def __init__(
        self,
        moon_service: MoonService,
        planet_service: PlanetService,
        sun_service: SunService,
        visibility_service: VisibilityService,
        star_service: Optional[StarService] = None,
        constellation_service: Optional[ConstellationService] = None,
    ) -> None:
        self._moon_service = moon_service
        self._planet_service = planet_service
        self._sun_service = sun_service
        self._visibility_service = visibility_service
        self._star_service = star_service or DefaultStarService()
        self._constellation_service = constellation_service or DefaultConstellationService(star_service=self._star_service)

    def get_moon_summary(self, context: ObservationContext) -> MoonPhase:
        """Return moon phase and visibility details for the given context."""
        return self._moon_service.get_moon_phase(context)

    def get_planetary_positions(
        self,
        context: ObservationContext,
    ) -> List[PlanetPosition]:
        """Return visible planet positions for the given context."""
        return self._planet_service.list_visible_planets(context)

    def get_solar_summary(self, context: ObservationContext) -> SolarState:
        """Return solar state data for the given context."""
        return self._sun_service.get_solar_state(context)

    def get_visibility_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        """Return visibility windows for requested objects and context."""
        return self._visibility_service.compute_visibility(context, object_names)

    def get_best_observation_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        """Return prioritized observation windows for the requested context."""
        return self._visibility_service.compute_best_observation_windows(
            context,
            object_names,
        )

    def get_star_positions(
        self,
        context: ObservationContext,
        min_altitude: float = 0.0,
    ) -> List[StarPosition]:
        """Return visible star positions for the given context."""
        return self._star_service.list_visible_stars(context, min_altitude=min_altitude)

    def get_constellations(
        self,
        context: ObservationContext,
        star_positions: Optional[List[StarPosition]] = None,
    ) -> List[ConstellationData]:
        """Return visible constellation data for the given context."""
        return self._constellation_service.list_constellations(context, star_positions=star_positions)

    def get_skymap_data(
        self,
        context: ObservationContext,
    ) -> SkyMapData:
        """Return aggregated sky map domain data containing planets, stars, constellations, moon, and sun."""
        moon = self.get_moon_summary(context)
        sun = self.get_solar_summary(context)
        planets = self.get_planetary_positions(context)
        stars = self.get_star_positions(context, min_altitude=-5.0)
        constellations = self.get_constellations(context, star_positions=stars)

        return SkyMapData(
            timestamp=context.timestamp,
            location=context.location,
            moon=moon,
            sun=sun,
            planets=planets,
            stars=stars,
            constellations=constellations,
        )
