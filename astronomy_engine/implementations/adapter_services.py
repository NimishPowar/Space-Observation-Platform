"""Adapter-backed astronomy service implementations."""

from __future__ import annotations

from typing import List, Optional

from astronomy_engine.adapters.skyfield_adapter import SkyfieldAdapter
from astronomy_engine.calculations.astronomy import (
    make_moon_phase,
    make_moon_visibility,
    make_planet_position,
    make_solar_state,
    make_visibility_window,
)
from astronomy_engine.core.domain import (
    MoonPhase,
    MoonVisibility,
    ObservationContext,
    PlanetPosition,
    SolarState,
    VisibilityWindow,
)
from astronomy_engine.services import MoonService, PlanetService, SunService, VisibilityService


class AdapterMoonService(MoonService):
    """Moon service that uses a Skyfield adapter for data acquisition."""

    def __init__(self, adapter: SkyfieldAdapter) -> None:
        self._adapter = adapter

    def get_moon_phase(self, context: ObservationContext) -> MoonPhase:
        state = self._adapter.get_moon_state(context)
        return make_moon_phase(state)

    def get_lunar_visibility(self, context: ObservationContext) -> MoonVisibility:
        raw_state = self._adapter.get_rise_set("Moon", context)
        return make_moon_visibility(raw_state)


class AdapterPlanetService(PlanetService):
    """Planet service that uses a Skyfield adapter for data acquisition."""

    _default_planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

    def __init__(self, adapter: SkyfieldAdapter) -> None:
        self._adapter = adapter

    def list_visible_planets(self, context: ObservationContext) -> List[PlanetPosition]:
        planets: List[PlanetPosition] = []
        for planet_name in self._default_planets:
            state = self._adapter.get_planet_state(planet_name, context)
            position = make_planet_position(state)
            if position.is_visible:
                planets.append(position)
        return planets

    def get_planet_position(
        self,
        name: str,
        context: ObservationContext,
    ) -> PlanetPosition:
        state = self._adapter.get_planet_state(name, context)
        return make_planet_position(state)


class AdapterSunService(SunService):
    """Sun service that uses a Skyfield adapter for data acquisition."""

    def __init__(self, adapter: SkyfieldAdapter) -> None:
        self._adapter = adapter

    def get_solar_state(self, context: ObservationContext) -> SolarState:
        state = self._adapter.get_sun_state(context)
        return make_solar_state(state)

    def get_sunrise_sunset(self, context: ObservationContext) -> SolarState:
        return self.get_solar_state(context)


class AdapterVisibilityService(VisibilityService):
    """Visibility service that uses a Skyfield adapter for data acquisition."""

    _default_objects = ["Moon", "Mars", "Venus", "Jupiter", "Saturn"]

    def __init__(self, adapter: SkyfieldAdapter) -> None:
        self._adapter = adapter

    def compute_visibility(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        names = object_names or self._default_objects
        windows: List[VisibilityWindow] = []
        for name in names:
            raw_state = self._adapter.get_rise_set(name, context)
            window = make_visibility_window(name, raw_state)
            if window.start is not None and window.end is not None:
                windows.append(window)
        return windows

    def compute_best_observation_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        return self.compute_visibility(context, object_names)

    def is_object_visible(
        self,
        object_name: str,
        context: ObservationContext,
    ) -> bool:
        raw_state = self._adapter.get_rise_set(object_name, context)
        return bool(raw_state.get("is_visible"))
