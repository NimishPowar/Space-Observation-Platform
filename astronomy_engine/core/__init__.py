"""Core astronomy engine package.

This package hosts the architecture-level core engine components, domain
models, and orchestration logic.
"""

from .engine import AstronomyEngine
from .domain import (
    CelestialEvent,
    Location,
    MoonPhase,
    MoonVisibility,
    ObservationContext,
    ObservationScore,
    PlanetPosition,
    SolarState,
    VisibilityWindow,
)

__all__ = [
    "AstronomyEngine",
    "Location",
    "MoonPhase",
    "MoonVisibility",
    "ObservationContext",
    "ObservationScore",
    "PlanetPosition",
    "SolarState",
    "VisibilityWindow",
    "CelestialEvent",
]
