"""Project settings and environment configuration.

This module centralizes environment-driven configuration for the platform.
The persistence layer is intentionally configured for MySQL and SQLAlchemy so
future repository and migration work remains isolated from business logic.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    project_name: str = "Space Observation Intelligence Platform"
    environment: str = os.getenv("ENVIRONMENT", "development")
    mysql_host: str = os.getenv("DB_HOST", "localhost")
    mysql_port: int = int(os.getenv("DB_PORT", "3306"))
    mysql_database: str = os.getenv("DB_NAME", "space_observation_platform")
    mysql_user: str = os.getenv("DB_USER", "space_user")
    mysql_password: str = os.getenv("DB_PASSWORD", "space_password")
    database_url: str = os.getenv(
        "DATABASE_URL",
        (
            "mysql+pymysql://"
            f"{os.getenv('DB_USER', 'space_user')}:{os.getenv('DB_PASSWORD', 'space_password')}"
            f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}"
            f"/{os.getenv('DB_NAME', 'space_observation_platform')}"
            "?charset=utf8mb4"
        ),
    )
    alembic_config_path: Path = Path(os.getenv("ALEMBIC_CONFIG_PATH", "alembic.ini"))
    data_dir: Path = Path(os.getenv("DATA_DIR", "datasets"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
