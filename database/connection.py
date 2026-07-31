"""Database connection placeholder.

This repository boundary remains separate from the astronomy engine and ETL
pipeline. SQLAlchemy-backed MySQL configuration is read from the central
settings module.
"""

from __future__ import annotations

from config.settings import settings


class DatabaseConnection:
    """Placeholder for database connection initialization."""

    def get_connection_string(self) -> str:
        """Return the configured database connection string."""
        return settings.database_url
