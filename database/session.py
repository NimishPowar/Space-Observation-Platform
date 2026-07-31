"""Database session management for the SQLAlchemy-backed persistence layer."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from config.settings import settings
from database.base import Base


class DatabaseSessionManager:
    """Provider for SQLAlchemy sessions and database lifecycle management."""

    def __init__(self, connection_url: str | None = None, engine: Engine | None = None) -> None:
        self._engine = engine or create_engine(
            connection_url or settings.database_url,
            pool_pre_ping=True,
            future=True,
        )
        self._session_factory = sessionmaker(
            bind=self._engine,
            class_=Session,
            autoflush=False,
            expire_on_commit=False,
        )

    @property
    def engine(self) -> Engine:
        """Return the configured SQLAlchemy engine."""
        return self._engine

    def get_session(self) -> Session:
        """Return a new database session."""
        return self._session_factory()

    def create_all(self) -> None:
        """Create all ORM tables on the configured engine."""
        Base.metadata.create_all(bind=self._engine)

    def dispose(self) -> None:
        """Dispose pooled database connections."""
        self._engine.dispose()


def get_session_dependency() -> Generator[Session, None, None]:
    """FastAPI-style dependency helper for SQLAlchemy sessions."""
    manager = DatabaseSessionManager()
    session = manager.get_session()
    try:
        yield session
    finally:
        session.close()
        manager.dispose()
