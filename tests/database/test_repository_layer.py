"""Unit tests for the repository layer and session management."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.models import CelestialEvent, EducationalCategory, EducationalContent, Planet, User
from database.repository import (
    CelestialEventRepository,
    EducationalContentRepository,
    PlanetRepository,
    UserRepository,
)
from database.session import DatabaseSessionManager


@pytest.fixture()
def session_manager() -> DatabaseSessionManager:
    """Create an in-memory SQLite-backed session manager for repository tests."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    manager = DatabaseSessionManager(engine=engine)
    yield manager
    manager.dispose()


def test_planet_repository_crud(session_manager: DatabaseSessionManager) -> None:
    """Verify that the planet repository can create, fetch, update, and delete records."""
    session = session_manager.get_session()
    repo = PlanetRepository(session)

    planet = Planet(
        name="mars",
        display_name="Mars",
        category="terrestrial",
        description="A core observation target.",
        mass_kg=6.39e23,
        radius_km=3389.5,
        semi_major_axis_au=1.52,
        orbital_period_days=687.0,
    )

    created = repo.create(planet)
    session.commit()

    fetched = repo.get_by_id(created.id)
    assert fetched is not None
    assert fetched.name == "mars"

    fetched.description = "Updated description"
    updated = repo.update(fetched)
    session.commit()
    assert updated.description == "Updated description"

    removed = repo.delete(created.id)
    session.commit()
    assert removed is True
    assert repo.get_by_id(created.id) is None

    session.close()


def test_educational_content_repository_filters_by_category(session_manager: DatabaseSessionManager) -> None:
    """Verify category-based repository filtering for educational content."""
    session = session_manager.get_session()
    category = EducationalCategory(
        slug="solar-system",
        name="Solar System",
        description="Reference material for solar-system learning.",
    )
    session.add(category)
    session.commit()

    content = EducationalContent(
        category_id=category.id,
        title="Mars Overview",
        slug="mars-overview",
        excerpt="An introduction to Mars.",
        body="Mars is the fourth planet from the Sun.",
        is_featured=True,
    )

    repo = EducationalContentRepository(session)
    repo.create(content)
    session.commit()

    results = repo.list_by_category(category.id)
    assert len(results) == 1
    assert results[0].slug == "mars-overview"

    session.close()


def test_educational_content_repository_find_by_object_name(session_manager: DatabaseSessionManager) -> None:
    """Verify object-name resolution for educational content lookups."""
    session = session_manager.get_session()
    category = EducationalCategory(
        slug="solar-system",
        name="Solar System",
        description="Reference material for solar-system learning.",
    )
    session.add(category)
    session.commit()

    content = EducationalContent(
        category_id=category.id,
        title="Mars Overview",
        slug="mars-overview",
        excerpt="An introduction to Mars.",
        body="Mars is the fourth planet from the Sun.",
        is_featured=True,
    )

    repo = EducationalContentRepository(session)
    repo.create(content)
    session.commit()

    by_slug = repo.find_by_object_name("mars-overview")
    assert by_slug is not None
    assert by_slug.slug == "mars-overview"

    by_object_name = repo.find_by_object_name("mars")
    assert by_object_name is not None
    assert by_object_name.slug == "mars-overview"

    session.close()


def test_celestial_event_repository_lists_upcoming_events(session_manager: DatabaseSessionManager) -> None:
    """Verify upcoming event filtering ordered by start time."""
    session = session_manager.get_session()
    now = datetime(2026, 7, 31, 12, 0, tzinfo=timezone.utc)

    session.add_all(
        [
            CelestialEvent(
                event_type="conjunction",
                title="Past Event",
                description="Already occurred.",
                starts_at=now - timedelta(days=1),
            ),
            CelestialEvent(
                event_type="opposition",
                title="Upcoming Event",
                description="Future event.",
                starts_at=now + timedelta(days=2),
            ),
        ]
    )
    session.commit()

    repo = CelestialEventRepository(session)
    results = repo.list_upcoming(from_time=now)

    assert len(results) == 1
    assert results[0].title == "Upcoming Event"

    session.close()


def test_user_repository_can_store_users(session_manager: DatabaseSessionManager) -> None:
    """Verify the user repository supports simple CRUD interactions."""
    session = session_manager.get_session()
    repo = UserRepository(session)

    user = User(
        username="observer_a",
        email="observer@test.local",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    created = repo.create(user)
    session.commit()

    fetched = repo.get_by_username("observer_a")
    assert fetched is not None
    assert fetched.email == "observer@test.local"

    session.close()
