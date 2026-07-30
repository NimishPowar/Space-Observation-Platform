"""Stub astronomy service implementations for initial architecture validation."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from astronomy_engine.core.domain import (
    MoonPhase,
    MoonVisibility,
    ObservationContext,
    PlanetPosition,
    SolarState,
    VisibilityWindow,
)
from astronomy_engine.services import (
    MoonService,
    PlanetService,
    SunService,
    VisibilityService,
)


class StubMoonService(MoonService):
    """Placeholder Moon service implementation."""

    def get_moon_phase(self, context: ObservationContext) -> MoonPhase:
        return MoonPhase(
            phase_name="Unknown",
            illumination=0.0,
            phase_angle=0.0,
            age_days=None,
            distance_km=None,
        )

    def get_lunar_visibility(self, context: ObservationContext) -> MoonVisibility:
        return MoonVisibility(
            rise_time=None,
            set_time=None,
            transit_time=None,
            altitude_at_transit=None,
            azimuth_rise=None,
            azimuth_set=None,
            is_visible=False,
        )


class StubPlanetService(PlanetService):
    """Placeholder Planet service implementation."""

    def list_visible_planets(self, context: ObservationContext) -> List[PlanetPosition]:
        return []

    def get_planet_position(
        self,
        name: str,
        context: ObservationContext,
    ) -> PlanetPosition:
        return PlanetPosition(
            object_name=name,
            right_ascension=0.0,
            declination=0.0,
            azimuth=None,
            altitude=None,
            distance_au=None,
            magnitude=None,
            is_visible=False,
        )


class StubSunService(SunService):
    """Placeholder Sun service implementation."""

    def get_solar_state(self, context: ObservationContext) -> SolarState:
        return SolarState(
            sunrise=None,
            sunset=None,
            solar_noon=None,
            day_length_minutes=None,
            elevation=None,
            azimuth=None,
            civil_twilight_begin=None,
            civil_twilight_end=None,
            nautical_twilight_begin=None,
            nautical_twilight_end=None,
            astronomical_twilight_begin=None,
            astronomical_twilight_end=None,
        )

    def get_sunrise_sunset(self, context: ObservationContext) -> SolarState:
        return self.get_solar_state(context)


class StubVisibilityService(VisibilityService):
    """Placeholder visibility service implementation."""

    def compute_visibility(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        return []

    def compute_best_observation_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        return []

    def is_object_visible(
        self,
        object_name: str,
        context: ObservationContext,
    ) -> bool:
        return False
