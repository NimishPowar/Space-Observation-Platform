"""Dependency providers for the backend API.

Provides application-scoped singletons such as the AstronomyEngine and
use-case instances. These are intentionally simple and suitable for the
initial development phases.
"""

from __future__ import annotations

from collections.abc import Generator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from astronomy_engine import create_astronomy_engine
from astronomy_engine.core.engine import AstronomyEngine
from backend.use_cases.astronomy_use_case import AstronomyUseCase
from backend.use_cases.events_use_case import EventsUseCase
from backend.use_cases.learn_use_case import LearnUseCase
from backend.use_cases.observation_planner import ObservationPlannerUseCase
from database.repository import (
    CelestialEventRepository,
    EducationalContentRepository,
    PlanetRepository,
)
from database.session import DatabaseSessionManager


@lru_cache(maxsize=1)
def get_engine() -> AstronomyEngine:
    """Return a singleton AstronomyEngine instance."""
    return create_astronomy_engine()


@lru_cache(maxsize=1)
def get_database_session_manager() -> DatabaseSessionManager:
    """Return a singleton session manager for the database layer."""
    return DatabaseSessionManager()


def get_database_session() -> Generator[Session, None, None]:
    """Return a database session using the shared session manager."""
    manager = get_database_session_manager()
    session = manager.get_session()
    try:
        yield session
    finally:
        session.close()


def get_planet_repository(session: Session) -> PlanetRepository:
    """Return a repository bound to the current DB session."""
    return PlanetRepository(session)


def get_educational_content_repository(session: Session) -> EducationalContentRepository:
    """Return an educational content repository bound to the current DB session."""
    return EducationalContentRepository(session)


def get_celestial_event_repository(session: Session) -> CelestialEventRepository:
    """Return a celestial event repository bound to the current DB session."""
    return CelestialEventRepository(session)


def get_astronomy_use_case() -> AstronomyUseCase:
    """Return a new AstronomyUseCase bound to the shared engine."""
    engine = get_engine()
    return AstronomyUseCase(engine=engine)


def get_observation_planner_use_case() -> ObservationPlannerUseCase:
    """Return a new ObservationPlannerUseCase bound to the shared engine."""
    return ObservationPlannerUseCase(engine=get_engine())


def get_learn_use_case(
    session: Session = Depends(get_database_session),
) -> LearnUseCase:
    """Return a LearnUseCase bound to the current database session."""
    return LearnUseCase(content_repository=EducationalContentRepository(session))


def get_events_use_case(
    session: Session = Depends(get_database_session),
) -> EventsUseCase:
    """Return an EventsUseCase bound to the current database session."""
    return EventsUseCase(event_repository=CelestialEventRepository(session))
