"""Repository abstractions for database access."""

from __future__ import annotations


class BaseRepository:
    """Base repository interface for data access operations."""

    def create(self, data: object) -> None:
        """Create a new record in the database."""
        pass

    def fetch(self, identifier: object) -> object:
        """Fetch a record by identifier."""
        pass
