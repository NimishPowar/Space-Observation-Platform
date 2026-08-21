"""Factory helpers for composing the astronomy engine."""

from __future__ import annotations

from astronomy_engine.core.engine import AstronomyEngine
from astronomy_engine.implementations import (
    AdapterMoonService,
    AdapterPlanetService,
    AdapterSunService,
    AdapterVisibilityService,
    SkyfieldRuntimeAdapter,
    StubMoonService,
    StubPlanetService,
    StubSunService,
    StubVisibilityService,
)
from astronomy_engine.services import DefaultConstellationService, DefaultStarService


def create_astronomy_engine(use_stubs: bool = False) -> AstronomyEngine:
    """Create a composed AstronomyEngine with runtime Skyfield services or stub test doubles."""
    star_service = DefaultStarService()
    constellation_service = DefaultConstellationService(star_service=star_service)

    if use_stubs:
        return AstronomyEngine(
            moon_service=StubMoonService(),
            planet_service=StubPlanetService(),
            sun_service=StubSunService(),
            visibility_service=StubVisibilityService(),
            star_service=star_service,
            constellation_service=constellation_service,
        )

    adapter = SkyfieldRuntimeAdapter()
    adapter.initialize()

    return AstronomyEngine(
        moon_service=AdapterMoonService(adapter=adapter),
        planet_service=AdapterPlanetService(adapter=adapter),
        sun_service=AdapterSunService(adapter=adapter),
        visibility_service=AdapterVisibilityService(adapter=adapter),
        star_service=star_service,
        constellation_service=constellation_service,
    )
