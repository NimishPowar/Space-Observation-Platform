"""Use cases for educational content served from the database."""

from __future__ import annotations

from dataclasses import dataclass

from database.repository import EducationalCategoryRepository, EducationalContentRepository


@dataclass(frozen=True)
class CategoryResult:
    """Educational taxonomy category representation."""

    slug: str
    name: str
    description: str | None


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

    def __init__(
        self,
        content_repository: EducationalContentRepository,
        category_repository: EducationalCategoryRepository | None = None,
    ) -> None:
        self._content_repository = content_repository
        self._category_repository = category_repository

    def list_categories(self) -> list[CategoryResult]:
        """Return all educational content categories."""
        if self._category_repository is None:
            return []
        categories = self._category_repository.list_all()
        return [
            CategoryResult(slug=c.slug, name=c.name, description=c.description)
            for c in categories
        ]

    def search_topics(
        self, query: str | None = None, category_slug: str | None = None
    ) -> list[LearnContentResult]:
        """Search topics by keyword query and/or category."""
        records = self._content_repository.search_topics(query=query, category_slug=category_slug)
        return [
            LearnContentResult(
                object_name=item.slug,
                slug=item.slug,
                title=item.title,
                excerpt=item.excerpt,
                body=item.body,
                category_slug=item.category.slug,
                category_name=item.category.name,
                source_url=item.source_url,
                is_featured=item.is_featured,
            )
            for item in records
        ]

    def list_featured(self) -> list[LearnContentResult]:
        """Return all featured educational topics."""
        records = self._content_repository.list_featured()
        return [
            LearnContentResult(
                object_name=item.slug,
                slug=item.slug,
                title=item.title,
                excerpt=item.excerpt,
                body=item.body,
                category_slug=item.category.slug,
                category_name=item.category.name,
                source_url=item.source_url,
                is_featured=item.is_featured,
            )
            for item in records
        ]

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
