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


def create_astronomy_engine() -> AstronomyEngine:
    """Create a composed AstronomyEngine with runtime Skyfield services."""
    adapter = SkyfieldRuntimeAdapter()
    adapter.initialize()

    return AstronomyEngine(
        moon_service=AdapterMoonService(adapter=adapter),
        planet_service=AdapterPlanetService(adapter=adapter),
        sun_service=AdapterSunService(adapter=adapter),
        visibility_service=AdapterVisibilityService(adapter=adapter),
    )
