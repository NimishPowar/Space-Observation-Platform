"""Unit tests for the observation planner backend use case."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import Mock

from astronomy_engine.core.domain import Location, ObservationContext, VisibilityWindow
from backend.use_cases.observation_planner import ObservationPlannerUseCase


def test_estimate_window_returns_ranked_scores() -> None:
    """Verify the planner converts engine visibility windows into scored observations."""
    context = ObservationContext(
        location=Location(latitude=12.0, longitude=77.0, elevation_meters=120.0),
        timestamp=datetime.now(timezone.utc),
        timezone="UTC",
        target_objects=["Mars"],
    )

    start_one = datetime.now(timezone.utc)
    end_one = start_one + timedelta(hours=2)
    start_two = start_one + timedelta(hours=4)
    end_two = start_two + timedelta(hours=1)

    engine = Mock()
    engine.get_best_observation_windows.return_value = [
        VisibilityWindow(
            object_name="Mars",
            start=start_one,
            end=end_one,
            max_elevation=72.0,
            azimuth_at_max=180.0,
            score=80.0,
            description="Excellent observation window",
        ),
        VisibilityWindow(
            object_name="Mars",
            start=start_two,
            end=end_two,
            max_elevation=24.0,
            azimuth_at_max=250.0,
            score=35.0,
            description="Lower-confidence window",
        ),
    ]

    use_case = ObservationPlannerUseCase(engine=engine)
    scores = use_case.estimate_window(context, object_names=["Mars"], limit=2)

    assert len(scores) == 2
    assert scores[0].score >= scores[1].score
    assert scores[0].object_name == "Mars"
    assert scores[0].metrics is not None
    assert scores[0].visibility_window is not None


def test_score_observation_alias_returns_results() -> None:
    """Verify that the planner score helper delegates cleanly to the same ranking path."""
    context = ObservationContext(
        location=Location(latitude=19.0, longitude=72.0, elevation_meters=50.0),
        timestamp=datetime.now(timezone.utc),
        timezone="UTC",
        target_objects=["Venus"],
    )
    engine = Mock()
    engine.get_best_observation_windows.return_value = [
        VisibilityWindow(
            object_name="Venus",
            start=datetime.now(timezone.utc),
            end=datetime.now(timezone.utc) + timedelta(minutes=120),
            max_elevation=60.0,
            azimuth_at_max=135.0,
            score=70.0,
            description="Good window",
        )
    ]

    use_case = ObservationPlannerUseCase(engine=engine)
    scores = use_case.score_observation(context, object_names=["Venus"], limit=1)

    assert len(scores) == 1
    assert scores[0].object_name == "Venus"
