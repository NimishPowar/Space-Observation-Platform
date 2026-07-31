"""Database package.

This package contains the database connection, ORM models, and repository
abstractions for the MySQL persistence layer.
"""

from database.base import Base
from database.models import (
    ApiCache,
    ApplicationSetting,
    CelestialEvent,
    EducationalCategory,
    EducationalContent,
    ObservationLog,
    Planet,
    User,
)
from database.repository import (
    ApiCacheRepository,
    ApplicationSettingRepository,
    CelestialEventRepository,
    EducationalCategoryRepository,
    EducationalContentRepository,
    ObservationLogRepository,
    PlanetRepository,
    SQLAlchemyRepository,
    UserRepository,
)
from database.session import DatabaseSessionManager

__all__ = [
    "ApiCache",
    "ApiCacheRepository",
    "ApplicationSetting",
    "ApplicationSettingRepository",
    "Base",
    "CelestialEvent",
    "CelestialEventRepository",
    "DatabaseSessionManager",
    "EducationalCategory",
    "EducationalCategoryRepository",
    "EducationalContent",
    "EducationalContentRepository",
    "ObservationLog",
    "ObservationLogRepository",
    "Planet",
    "PlanetRepository",
    "SQLAlchemyRepository",
    "User",
    "UserRepository",
]
