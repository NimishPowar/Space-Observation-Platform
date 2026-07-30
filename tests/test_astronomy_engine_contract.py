"""Tests for the Astronomy Engine contract and backend integration."""

from __future__ import annotations

from astronomy_engine import create_astronomy_engine
from backend.use_cases.astronomy_use_case import AstronomyUseCase
from astronomy_engine.core.domain import Location, ObservationContext
from datetime import datetime, timezone


def test_astronomy_engine_composition() -> None:
    engine = create_astronomy_engine()
    assert engine is not None


def test_backend_use_case_can_delegate_to_engine() -> None:
    engine = create_astronomy_engine()
    use_case = AstronomyUseCase(engine=engine)
    context = ObservationContext(
        location=Location(latitude=0.0, longitude=0.0),
        timestamp=datetime.now(timezone.utc),
    )

    moon_summary = use_case.get_moon_summary(context)
    assert moon_summary.phase_name != ""
    assert moon_summary.illumination >= 0.0

    solar_summary = use_case.get_solar_summary(context)
    assert solar_summary.elevation is not None

    planet_positions = use_case.get_planetary_positions(context)
    assert isinstance(planet_positions, list)

    visibility_windows = use_case.get_visibility_windows(context, ["Moon"])
    assert isinstance(visibility_windows, list)
