"""Database connection placeholder.

This repository boundary remains separate from the astronomy engine and ETL
pipeline. SQLAlchemy-backed MySQL configuration is read from the central
settings module.
"""

from __future__ import annotations

from config.settings import settings
from database.session import DatabaseSessionManager


class DatabaseConnection:
    """Create a reusable database session manager from the configured settings."""

    def __init__(self, connection_url: str | None = None) -> None:
        self._connection_url = connection_url or settings.database_url

    def get_connection_string(self) -> str:
        """Return the configured database connection string."""
        return self._connection_url

    def get_session_manager(self) -> DatabaseSessionManager:
        """Return a session manager for the configured connection."""
        return DatabaseSessionManager(connection_url=self._connection_url)
