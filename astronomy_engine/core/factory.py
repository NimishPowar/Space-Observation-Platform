"""Factory helpers for composing the astronomy engine."""

from __future__ import annotations

from astronomy_engine.core.engine import AstronomyEngine
from astronomy_engine.implementations import (
    AdapterMoonService,
    AdapterPlanetService,
    AdapterSunService,
    AdapterVisibilityService,
    SkyfieldRuntimeAdapter,
)
from astronomy_engine.services import DefaultConstellationService, DefaultStarService


def create_astronomy_engine() -> AstronomyEngine:
    """Create a composed AstronomyEngine with runtime Skyfield services."""
    adapter = SkyfieldRuntimeAdapter()
    adapter.initialize()

    star_service = DefaultStarService()
    constellation_service = DefaultConstellationService(star_service=star_service)

    return AstronomyEngine(
        moon_service=AdapterMoonService(adapter=adapter),
        planet_service=AdapterPlanetService(adapter=adapter),
        sun_service=AdapterSunService(adapter=adapter),
        visibility_service=AdapterVisibilityService(adapter=adapter),
        star_service=star_service,
        constellation_service=constellation_service,
    )
