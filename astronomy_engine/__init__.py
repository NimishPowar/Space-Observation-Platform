"""Astronomy engine package.

This package contains the core astronomy calculation engine, service
interfaces, and adapter integration for astronomical computations.
"""

from .core.factory import create_astronomy_engine
from .core.engine import AstronomyEngine
from .core.domain import (
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
    "CelestialEvent",
    "Location",
    "MoonPhase",
    "MoonVisibility",
    "ObservationContext",
    "ObservationScore",
    "PlanetPosition",
    "SolarState",
    "VisibilityWindow",
    "create_astronomy_engine",
]
