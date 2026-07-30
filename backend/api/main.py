"""Backend API application entrypoint.

This module defines the backend application factory and the integration
boundary between the backend service and the astronomy engine.
"""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.routes import router


def create_app() -> FastAPI:
    """Create an application instance and register API routes."""
    app = FastAPI(title="Space Observation Intelligence Platform API")
    app.include_router(router, prefix="/api")
    return app


app = create_app()
