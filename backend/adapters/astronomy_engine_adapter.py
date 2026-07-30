"""Backend adapter for astronomy engine integration."""

from __future__ import annotations

from astronomy_engine.core.engine import AstronomyEngine


class AstronomyEngineAdapter:
    """Simple adapter that exposes the astronomy engine to backend use cases."""

    def __init__(self, engine: AstronomyEngine) -> None:
        self.engine = engine
