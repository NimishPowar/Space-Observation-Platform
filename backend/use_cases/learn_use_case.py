"""Use cases for educational content served from the database."""

from __future__ import annotations

from dataclasses import dataclass

from database.repository import EducationalContentRepository


@dataclass(frozen=True)
class LearnContentResult:
    """Database-backed educational content for a requested object."""

    object_name: str
    slug: str
    title: str
    excerpt: str | None
    body: str | None
    category_slug: str
    category_name: str
    source_url: str | None
    is_featured: bool


class LearnUseCase:
    """Retrieve educational content without hardcoded text in the API layer."""

    def __init__(self, content_repository: EducationalContentRepository) -> None:
        self._content_repository = content_repository

    def get_content_for_object(self, object_name: str) -> LearnContentResult | None:
        """Return educational content matching the requested object name, if any."""
        content = self._content_repository.find_by_object_name(object_name)
        if content is None:
            return None

        return LearnContentResult(
            object_name=object_name,
            slug=content.slug,
            title=content.title,
            excerpt=content.excerpt,
            body=content.body,
            category_slug=content.category.slug,
            category_name=content.category.name,
            source_url=content.source_url,
            is_featured=content.is_featured,
        )
