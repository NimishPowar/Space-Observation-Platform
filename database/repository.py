"""Repository abstractions and concrete SQLAlchemy implementations.

The repository layer is intentionally separated from the astronomy engine and
keeps persistence concerns behind a stable interface that the backend can use
without directly touching the database session.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from database.models import (
    ApiCache,
    ApplicationSetting,
    CelestialEvent,
    EducationalCategory,
    EducationalContent,
    NasaApod,
    ObservationLog,
    Planet,
    User,
)

ModelT = TypeVar("ModelT")


class BaseRepository(ABC, Generic[ModelT]):
    """Abstract repository contract for CRUD operations."""

    @abstractmethod
    def create(self, entity: ModelT) -> ModelT:
        """Persist a new entity."""

    @abstractmethod
    def get_by_id(self, identifier: int) -> ModelT | None:
        """Fetch an entity by primary key."""

    @abstractmethod
    def list_all(self) -> list[ModelT]:
        """Return all persisted entities."""

    @abstractmethod
    def update(self, entity: ModelT) -> ModelT:
        """Update an existing entity in place."""

    @abstractmethod
    def delete(self, identifier: int) -> bool:
        """Delete an entity by primary key and return whether it was removed."""


class SQLAlchemyRepository(BaseRepository[ModelT]):
    """Generic SQLAlchemy repository that can back any table model."""

    def __init__(self, session: Session, model: type[ModelT]) -> None:
        self._session = session
        self._model = model

    def create(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        self._session.flush()
        return entity

    def get_by_id(self, identifier: int) -> ModelT | None:
        statement = select(self._model).where(self._model.id == identifier)
        return cast(ModelT | None, self._session.scalar(statement))

    def list_all(self) -> list[ModelT]:
        statement = select(self._model)
        return list(self._session.scalars(statement).all())

    def update(self, entity: ModelT) -> ModelT:
        self._session.merge(entity)
        self._session.flush()
        return entity

    def delete(self, identifier: int) -> bool:
        entity = self.get_by_id(identifier)
        if entity is None:
            return False
        self._session.delete(entity)
        self._session.flush()
        return True


class PlanetRepository(SQLAlchemyRepository[Planet]):
    """Repository for planet reference data."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, Planet)

    def get_by_name(self, name: str) -> Planet | None:
        statement = select(Planet).where(Planet.name == name)
        return self._session.scalar(statement)


class CelestialEventRepository(SQLAlchemyRepository[CelestialEvent]):
    """Repository for event reference records."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, CelestialEvent)

    def list_upcoming(self, from_time: datetime, limit: int = 50) -> list[CelestialEvent]:
        """Return upcoming events starting at or after the given timestamp."""
        statement = (
            select(CelestialEvent)
            .options(joinedload(CelestialEvent.planet))
            .where(CelestialEvent.starts_at >= from_time)
            .order_by(CelestialEvent.starts_at.asc())
            .limit(limit)
        )
        return list(self._session.scalars(statement).unique().all())


class EducationalCategoryRepository(SQLAlchemyRepository[EducationalCategory]):
    """Repository for educational categories."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, EducationalCategory)

    def get_by_slug(self, slug: str) -> EducationalCategory | None:
        statement = select(EducationalCategory).where(EducationalCategory.slug == slug)
        return self._session.scalar(statement)


class EducationalContentRepository(SQLAlchemyRepository[EducationalContent]):
    """Repository for educational content records."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, EducationalContent)

    def list_by_category(self, category_id: int) -> list[EducationalContent]:
        statement = select(EducationalContent).where(EducationalContent.category_id == category_id)
        return list(self._session.scalars(statement).all())

    def get_by_slug(self, slug: str) -> EducationalContent | None:
        statement = (
            select(EducationalContent)
            .options(joinedload(EducationalContent.category))
            .where(EducationalContent.slug == slug)
        )
        return self._session.scalar(statement)

    def list_all(self) -> list[EducationalContent]:
        """Return all educational content records."""
        statement = select(EducationalContent).options(joinedload(EducationalContent.category)).order_by(EducationalContent.title.asc())
        return list(self._session.scalars(statement).all())

    def list_featured(self) -> list[EducationalContent]:
        """Return featured educational content records."""
        statement = (
            select(EducationalContent)
            .options(joinedload(EducationalContent.category))
            .where(EducationalContent.is_featured == True)
            .order_by(EducationalContent.title.asc())
        )
        return list(self._session.scalars(statement).all())

    def find_by_object_name(self, object_name: str) -> EducationalContent | None:
        """Resolve educational content from a route object name or slug."""
        normalized = object_name.strip().lower().replace(" ", "-")
        if not normalized:
            return None

        exact_match = self.get_by_slug(normalized)
        if exact_match is not None:
            return exact_match

        for suffix in ("-overview", "-guide"):
            slug_candidate = f"{normalized}{suffix}"
            match = self.get_by_slug(slug_candidate)
            if match is not None:
                return match

        prefix_statement = (
            select(EducationalContent)
            .options(joinedload(EducationalContent.category))
            .where(EducationalContent.slug.like(f"{normalized}%"))
            .order_by(EducationalContent.slug.asc())
            .limit(1)
        )
        return self._session.scalar(prefix_statement)

    def search_topics(
        self, query: str | None = None, category_slug: str | None = None
    ) -> list[EducationalContent]:
        """Search educational content by keyword query and/or category slug."""
        statement = select(EducationalContent).options(joinedload(EducationalContent.category))

        if category_slug:
            statement = statement.join(EducationalContent.category).where(
                EducationalCategory.slug == category_slug
            )

        if query:
            pattern = f"%{query.strip()}%"
            statement = statement.where(
                or_(
                    EducationalContent.title.ilike(pattern),
                    EducationalContent.excerpt.ilike(pattern),
                    EducationalContent.body.ilike(pattern),
                    EducationalContent.slug.ilike(pattern),
                )
            )

        statement = statement.order_by(EducationalContent.title.asc())
        return list(self._session.scalars(statement).all())


class ObservationLogRepository(SQLAlchemyRepository[ObservationLog]):
    """Repository for user observation logs."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, ObservationLog)

    def list_for_user(self, user_id: int) -> list[ObservationLog]:
        statement = select(ObservationLog).where(ObservationLog.user_id == user_id)
        return list(self._session.scalars(statement).all())


class ApiCacheRepository(SQLAlchemyRepository[ApiCache]):
    """Repository for cached remote API payloads."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, ApiCache)

    def get_by_request_key(self, request_key: str) -> ApiCache | None:
        statement = select(ApiCache).where(ApiCache.request_key == request_key)
        return self._session.scalar(statement)


class ApplicationSettingRepository(SQLAlchemyRepository[ApplicationSetting]):
    """Repository for setting and preference storage."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, ApplicationSetting)

    def get_by_key(self, key: str) -> ApplicationSetting | None:
        statement = select(ApplicationSetting).where(ApplicationSetting.key == key)
        return self._session.scalar(statement)


class UserRepository(SQLAlchemyRepository[User]):
    """Repository for current and future application users."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, User)

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self._session.scalar(statement)


class NasaApodRepository(SQLAlchemyRepository[NasaApod]):
    """Repository for NASA APOD cached entries."""

    def __init__(self, session: Session) -> None:
        super().__init__(session, NasaApod)

    def get_by_date(self, apod_date: str) -> NasaApod | None:
        """Get APOD entry by date string (YYYY-MM-DD)."""
        statement = select(NasaApod).where(NasaApod.apod_date == apod_date)
        return self._session.scalar(statement)

    def get_latest(self, limit: int = 10) -> list[NasaApod]:
        """Get the most recent APOD entries."""
        statement = (
            select(NasaApod)
            .order_by(NasaApod.apod_date.desc())
            .limit(limit)
        )
        return list(self._session.scalars(statement).all())

    def upsert(self, entry: NasaApod) -> NasaApod:
        """Insert or update an APOD entry by date."""
        existing = self.get_by_date(entry.apod_date)
        if existing is not None:
            existing.title = entry.title
            existing.explanation = entry.explanation
            existing.url = entry.url
            existing.hdurl = entry.hdurl
            existing.media_type = entry.media_type
            existing.copyright_text = entry.copyright_text
            existing.thumbnail_url = entry.thumbnail_url
            self._session.flush()
            return existing
        self._session.add(entry)
        self._session.flush()
        return entry
