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


def test_discovery_categories_endpoint(client, db_session) -> None:
    category = EducationalCategory(
        slug="deep-space",
        name="Deep Space & Cosmology",
        description="Galaxies and cosmology.",
    )
    db_session.add(category)
    db_session.commit()

    response = client.get("/api/discovery/categories")
    assert response.status_code == 200
    payload = response.json()
    assert any(c["slug"] == "deep-space" for c in payload)


def test_discovery_topics_search(client, db_session) -> None:
    category = EducationalCategory(
        slug="stellar-astronomy",
        name="Stars & Nebulae",
        description="Stellar phenomena.",
    )
    db_session.add(category)
    db_session.commit()

    content = EducationalContent(
        category_id=category.id,
        title="Black Holes: Gravity's Ultimate Triumph",
        slug="black-holes",
        excerpt="Extreme gravitational regions.",
        body="Black holes collapse under intense gravity.",
        is_featured=True,
    )
    db_session.add(content)
    db_session.commit()

    response = client.get("/api/discovery/topics?query=Black%20Holes")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert payload[0]["slug"] == "black-holes"


def test_discovery_moon_phase_endpoint(client) -> None:
    response = client.get("/api/discovery/moon-phase?latitude=12.97&longitude=77.59&day_offset=2")
    assert response.status_code == 200
    payload = response.json()
    assert "phase_name" in payload
    assert "illumination" in payload
    assert "age_days" in payload
    assert "unicode_symbol" in payload
    assert "prev_phase_name" in payload
    assert "next_phase_name" in payload
