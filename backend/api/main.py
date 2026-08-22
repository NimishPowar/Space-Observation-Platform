"""Backend API application entrypoint.

This module defines the backend application factory and the integration
boundary between the backend service and the astronomy engine.
"""

from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router


def create_app() -> FastAPI:
    """Create an application instance and register API routes and static component mounts."""
    app = FastAPI(title="Space Observation Intelligence Platform API")
    app.include_router(router, prefix="/api")

    root_dir = Path(__file__).resolve().parent.parent.parent
    solarsystem_dir = root_dir / "solarsystem"
    moonphase_dir = root_dir / "moonphase"

    if solarsystem_dir.is_dir() and any(solarsystem_dir.iterdir()):
        app.mount("/static/solarsystem", StaticFiles(directory=str(solarsystem_dir), html=True), name="solarsystem")

    if moonphase_dir.is_dir() and any(moonphase_dir.iterdir()):
        app.mount("/static/moonphase", StaticFiles(directory=str(moonphase_dir), html=True), name="moonphase")

    return app


app = create_app()
