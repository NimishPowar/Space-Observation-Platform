"""Unit tests for LearnUseCase."""

from __future__ import annotations

from backend.use_cases.learn_use_case import LearnUseCase
from database.models import EducationalCategory, EducationalContent
from database.repository import EducationalContentRepository


def test_learn_use_case_returns_content_by_slug(db_session) -> None:
    category = EducationalCategory(
        slug="solar-system",
        name="Solar System",
        description="Solar system learning material.",
    )
    db_session.add(category)
    db_session.commit()

    content = EducationalContent(
        category_id=category.id,
        title="Mars Overview",
        slug="mars-overview",
        excerpt="An introduction to Mars.",
        body="Mars is the fourth planet from the Sun.",
        source_url="https://example.org/mars",
        is_featured=True,
    )
    db_session.add(content)
    db_session.commit()

    use_case = LearnUseCase(content_repository=EducationalContentRepository(db_session))
    result = use_case.get_content_for_object("mars-overview")

    assert result is not None
    assert result.slug == "mars-overview"
    assert result.title == "Mars Overview"
    assert result.category_slug == "solar-system"
    assert result.body == "Mars is the fourth planet from the Sun."


def test_learn_use_case_resolves_object_name_to_slug(db_session) -> None:
    category = EducationalCategory(
        slug="planetary-science",
        name="Planetary Science",
        description="Planetary science learning material.",
    )
    db_session.add(category)
    db_session.commit()

    content = EducationalContent(
        category_id=category.id,
        title="Jupiter Guide",
        slug="jupiter-guide",
        excerpt="A guide to Jupiter.",
        body="Jupiter is the largest planet in the solar system.",
        is_featured=False,
    )
    db_session.add(content)
    db_session.commit()

    use_case = LearnUseCase(content_repository=EducationalContentRepository(db_session))
    result = use_case.get_content_for_object("jupiter")

    assert result is not None
    assert result.slug == "jupiter-guide"
    assert result.object_name == "jupiter"


def test_learn_use_case_returns_none_when_content_missing(db_session) -> None:
    use_case = LearnUseCase(content_repository=EducationalContentRepository(db_session))
    assert use_case.get_content_for_object("unknown-object") is None
