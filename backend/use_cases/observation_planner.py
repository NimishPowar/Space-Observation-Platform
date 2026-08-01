"""Observation planner use case for ranking visibility windows.

This use case composes the astronomy engine's visibility data into stable
backend-facing observation scores without leaking Skyfield types into the API
layer.
"""

from __future__ import annotations

from datetime import datetime

from astronomy_engine.core.domain import ObservationContext, ObservationScore, VisibilityWindow
from astronomy_engine.core.engine import AstronomyEngine


class ObservationPlannerUseCase:
    """Rank observation opportunities based on the astronomy engine output."""

    def __init__(self, engine: AstronomyEngine) -> None:
        self._engine = engine

    def estimate_window(
        self,
        context: ObservationContext,
        object_names: list[str] | None = None,
        limit: int = 5,
    ) -> list[ObservationScore]:
        """Return ranked observation scores for the best visibility windows."""
        windows = self._engine.get_best_observation_windows(context, object_names)
        ranked_windows = sorted(
            (window for window in windows if window.start and window.end),
            key=self._sort_key,
            reverse=True,
        )[:limit]

        return [self._build_score(context, window) for window in ranked_windows]

    def score_observation(
        self,
        context: ObservationContext,
        object_names: list[str] | None = None,
        limit: int = 5,
    ) -> list[ObservationScore]:
        """Compute ranked observation scores using visibility window heuristics."""
        return self.estimate_window(context, object_names=object_names, limit=limit)

    @staticmethod
    def _sort_key(window: VisibilityWindow) -> tuple[float, float, float]:
        duration_minutes = ObservationPlannerUseCase._duration_minutes(window.start, window.end)
        max_elevation = float(window.max_elevation or 0.0)
        score = float(window.score or 0.0)
        return (score, max_elevation, duration_minutes)

    @staticmethod
    def _duration_minutes(start: datetime, end: datetime) -> float:
        duration = end - start
        return max(duration.total_seconds() / 60.0, 0.0)

    @staticmethod
    def _build_score(context: ObservationContext, window: VisibilityWindow) -> ObservationScore:
        duration_minutes = ObservationPlannerUseCase._duration_minutes(window.start, window.end)
        max_elevation = float(window.max_elevation or 0.0)
        score_base = float(window.score or 0.0)

        elevation_component = min(max_elevation, 90.0) / 90.0 * 45.0
        duration_component = min(duration_minutes, 180.0) / 180.0 * 40.0
        score_component = min(score_base, 100.0) * 0.15
        total_score = round(min(100.0, elevation_component + duration_component + score_component), 2)

        if total_score >= 80.0:
            reason = "Strong visibility potential with high altitude and long observation duration."
        elif total_score >= 60.0:
            reason = "Moderate observing opportunity with acceptable altitude and duration."
        else:
            reason = "Lower-confidence visibility window; consider a different target or time window."

        return ObservationScore(
            object_name=window.object_name,
            score=total_score,
            score_reason=reason,
            visibility_window=window,
            metrics={
                "max_elevation": round(max_elevation, 2),
                "duration_minutes": round(duration_minutes, 2),
                "base_score": round(score_base, 2),
            },
        )
