"""Shared fixtures for backend API and use-case tests."""

from __future__ import annotations

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from backend.api.dependencies import get_database_session
from backend.api.main import create_app
from database.base import Base
from database.session import DatabaseSessionManager


@pytest.fixture()
def session_manager() -> Generator[DatabaseSessionManager, None, None]:
    """Create an in-memory SQLite-backed session manager for backend tests."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)
    manager = DatabaseSessionManager(engine=engine)
    yield manager
    manager.dispose()


@pytest.fixture()
def db_session(session_manager: DatabaseSessionManager):
    """Yield a database session bound to the in-memory test database."""
    session = session_manager.get_session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(session_manager: DatabaseSessionManager) -> Generator[TestClient, None, None]:
    """Return a FastAPI test client with the database session overridden."""
    app = create_app()

    def override_get_database_session() -> Generator:
        session = session_manager.get_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_database_session] = override_get_database_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
