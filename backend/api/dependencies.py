"""Dependency providers for the backend API.

Provides application-scoped singletons such as the AstronomyEngine and
use-case instances. These are intentionally simple and suitable for the
initial development phases.
"""

from __future__ import annotations

from functools import lru_cache

from astronomy_engine import create_astronomy_engine
from astronomy_engine.core.engine import AstronomyEngine
from backend.use_cases.astronomy_use_case import AstronomyUseCase


@lru_cache(maxsize=1)
def get_engine() -> AstronomyEngine:
    """Return a singleton AstronomyEngine instance."""
    return create_astronomy_engine()


def get_astronomy_use_case() -> AstronomyUseCase:
    """Return a new AstronomyUseCase bound to the shared engine."""
    engine = get_engine()
    return AstronomyUseCase(engine=engine)
