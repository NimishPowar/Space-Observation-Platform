"""API tests for the Learn endpoint."""

from __future__ import annotations

from database.models import EducationalCategory, EducationalContent


def test_learn_endpoint_returns_database_content(client, db_session) -> None:
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

    response = client.get("/api/learn/mars-overview")

    assert response.status_code == 200
    payload = response.json()
    assert payload["slug"] == "mars-overview"
    assert payload["title"] == "Mars Overview"
    assert payload["category_slug"] == "solar-system"
    assert payload["body"] == "Mars is the fourth planet from the Sun."


def test_learn_endpoint_resolves_object_name(client, db_session) -> None:
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

    response = client.get("/api/learn/jupiter")

    assert response.status_code == 200
    assert response.json()["slug"] == "jupiter-guide"


def test_learn_endpoint_returns_404_when_content_missing(client) -> None:
    response = client.get("/api/learn/unknown-object")

    assert response.status_code == 404
    assert "No educational content found" in response.json()["detail"]
