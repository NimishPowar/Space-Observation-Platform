"""Project settings and environment configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_name: str = "Space Observation Intelligence Platform"
    environment: str = os.getenv("ENVIRONMENT", "development")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/space_observation_platform",
    )
    data_dir: Path = Path(os.getenv("DATA_DIR", "datasets"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
