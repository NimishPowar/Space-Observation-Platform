"""Static seeders for normalized reference data.

These seeders are intended for reference data such as planets and educational
categories. They are intentionally data-only and do not implement ETL logic.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from database.models import EducationalCategory, Planet


def seed_planets(session: Session) -> None:
    """Seed a minimal set of planetary reference records."""
    reference_planets = [
        {
            "name": "mars",
            "display_name": "Mars",
            "category": "terrestrial",
            "description": "The red planet used as a core observation target.",
            "mass_kg": 6.39e23,
            "radius_km": 3389.5,
            "semi_major_axis_au": 1.52,
            "orbital_period_days": 687.0,
            "mean_density_g_cm3": 3.93,
            "source_url": "https://nasa.gov",
        },
        {
            "name": "jupiter",
            "display_name": "Jupiter",
            "category": "gas_giant",
            "description": "A high-visibility gas giant with strong observational interest.",
            "mass_kg": 1.898e27,
            "radius_km": 69911.0,
            "semi_major_axis_au": 5.20,
            "orbital_period_days": 4332.59,
            "mean_density_g_cm3": 1.33,
            "source_url": "https://nasa.gov",
        },
    ]

    for payload in reference_planets:
        existing = session.query(Planet).filter_by(name=payload["name"]).first()
        if existing is None:
            session.add(Planet(**payload))


def seed_educational_categories(session: Session) -> None:
    """Seed foundational educational taxonomy values."""
    categories = [
        {
            "slug": "solar-system",
            "name": "Solar System",
            "description": "Reference material describing the solar system.",
        },
        {
            "slug": "planetary-science",
            "name": "Planetary Science",
            "description": "Educational data about planets and planetary behaviors.",
        },
    ]

    for payload in categories:
        existing = session.query(EducationalCategory).filter_by(slug=payload["slug"]).first()
        if existing is None:
            session.add(EducationalCategory(**payload))


def seed_reference_data(session: Session) -> None:
    """Run all static seeders into one session transaction."""
    seed_planets(session)
    seed_educational_categories(session)
    session.commit()
