"""Backend API application entrypoint.

This module defines the backend application factory and the integration
boundary between the backend service and the astronomy engine.
"""

from __future__ import annotations

from fastapi import FastAPI

from astronomy_engine.core.engine import AstronomyEngine


def create_app(engine: AstronomyEngine) -> FastAPI:
    """Create an application instance with engine integration.

    The application is intentionally lightweight and does not define any
    endpoints in this phase.
    """
    app = FastAPI(title="Space Observation Intelligence Platform API")
    app.state.engine = engine
    return app
