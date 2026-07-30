"""Runtime Skyfield adapter implementation."""

from __future__ import annotations

from astronomy_engine.adapters.skyfield_adapter import SkyfieldAdapter
from astronomy_engine.calculations.astronomy import (
    calculate_moon_state,
    calculate_planet_state,
    calculate_rise_set,
    calculate_solar_state,
    create_topocentric_location,
    load_ephemeris,
    load_timescale,
)
from astronomy_engine.core.domain import ObservationContext


class SkyfieldRuntimeAdapter(SkyfieldAdapter):
    """Skyfield adapter implementation using the skyfield library."""

    def __init__(self) -> None:
        self._ephemeris = None
        self._ts = None

    def initialize(self) -> None:
        self._ephemeris = load_ephemeris()
        self._ts = load_timescale()

    def _assert_ready(self) -> None:
        if self._ephemeris is None or self._ts is None:
            raise RuntimeError("Skyfield adapter has not been initialized.")

    def get_planet_state(self, planet_name: str, context: ObservationContext) -> object:
        self._assert_ready()
        observer = create_topocentric_location(self._ephemeris, context.location)
        return calculate_planet_state(
            self._ephemeris,
            self._ts,
            observer,
            planet_name,
            context.timestamp,
        )

    def get_moon_state(self, context: ObservationContext) -> object:
        self._assert_ready()
        observer = create_topocentric_location(self._ephemeris, context.location)
        return calculate_moon_state(
            self._ephemeris,
            self._ts,
            observer,
            context.timestamp,
        )

    def get_sun_state(self, context: ObservationContext) -> object:
        self._assert_ready()
        observer = create_topocentric_location(self._ephemeris, context.location)
        return calculate_solar_state(
            self._ephemeris,
            self._ts,
            observer,
            context.timestamp,
        )

    def get_rise_set(self, body_name: str, context: ObservationContext) -> object:
        self._assert_ready()
        observer = create_topocentric_location(self._ephemeris, context.location)
        return calculate_rise_set(
            self._ephemeris,
            self._ts,
            observer,
            body_name,
            context.timestamp,
        )
