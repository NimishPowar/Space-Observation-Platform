"""Analytics dashboard engine for generating observation analytics and telemetry summaries."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from astronomy_engine.core.domain import Location, ObservationContext
from astronomy_engine.core.engine import AstronomyEngine
from database.models import CelestialEvent, NasaApod


class AnalyticsDashboard:
    """Composition engine for astronomical observation analytics and visualization data."""

    def __init__(self, engine: AstronomyEngine | None = None) -> None:
        if engine is None:
            from astronomy_engine import create_astronomy_engine
            self._engine = create_astronomy_engine()
        else:
            self._engine = engine

    def generate_summary(
        self,
        latitude: float,
        longitude: float,
        timestamp: Optional[datetime] = None,
        elevation: Optional[float] = None,
        db_session: Optional[Session] = None,
    ) -> Dict[str, Any]:
        """Build structured analytics metrics, category distributions, and elevation trajectories."""
        ts = timestamp or datetime.now(timezone.utc)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        context = ObservationContext(
            location=Location(latitude=latitude, longitude=longitude, elevation_meters=elevation or 0.0),
            timestamp=ts,
            timezone=str(ts.tzinfo),
        )

        # 1. Target Suitability Scores & Categories
        targets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Moon"]
        scores = []
        category_counts: Dict[str, int] = {
            "Terrestrial Planets": 0,
            "Gas Giants": 0,
            "Lunar": 0,
            "Deep-Sky & Other": 0,
        }

        planet_states = self._engine.get_planetary_positions(context)
        for p in planet_states:
            alt = float(p.altitude or 0.0)
            name = p.object_name

            # Determine category
            if name in ["Mercury", "Venus", "Mars"]:
                cat = "Terrestrial Planets"
            elif name in ["Jupiter", "Saturn", "Uranus", "Neptune"]:
                cat = "Gas Giants"
            else:
                cat = "Deep-Sky & Other"

            category_counts[cat] = category_counts.get(cat, 0) + 1

            # Suitability score algorithm (0-100) based on elevation and visibility
            suitability = round(max(0.0, min(100.0, (alt + 15.0) / 105.0 * 100.0)), 1) if p.is_visible else round(max(0.0, alt + 15.0), 1)
            scores.append({
                "object_name": name,
                "score": suitability,
                "altitude": round(alt, 1),
                "is_visible": bool(p.is_visible),
                "category": cat,
            })

        # Add Moon
        lunar_vis = self._engine.get_lunar_visibility(context)
        moon_alt = float(lunar_vis.altitude_at_transit or 0.0)
        category_counts["Lunar"] += 1
        scores.append({
            "object_name": "Moon",
            "score": round(max(0.0, min(100.0, (moon_alt + 15.0) / 105.0 * 100.0)), 1) if lunar_vis.is_visible else 0.0,
            "altitude": round(moon_alt, 1),
            "is_visible": bool(lunar_vis.is_visible),
            "category": "Lunar",
        })

        scores.sort(key=lambda s: s["score"], reverse=True)

        # 2. 24-Hour Hourly Elevation Trajectories
        elevation_trajectories: List[Dict[str, Any]] = []
        start_hour = datetime(ts.year, ts.month, ts.day, tzinfo=timezone.utc)
        trajectory_bodies = ["Venus", "Mars", "Jupiter", "Saturn", "Moon"]

        for body in trajectory_bodies:
            hourly_points = []
            for h in range(24):
                step_ts = start_hour + timedelta(hours=h)
                step_ctx = ObservationContext(
                    location=context.location,
                    timestamp=step_ts,
                    timezone=context.timezone,
                )
                if body == "Moon":
                    m_vis = self._engine.get_lunar_visibility(step_ctx)
                    hourly_points.append({"hour": step_ts.strftime("%H:00"), "altitude": round(float(m_vis.altitude_at_transit or 0.0), 1)})
                else:
                    p_states = self._engine.get_planetary_positions(step_ctx)
                    match_p = next((p for p in p_states if p.object_name == body), None)
                    alt_val = float(match_p.altitude or 0.0) if match_p else 0.0
                    hourly_points.append({"hour": step_ts.strftime("%H:00"), "altitude": round(alt_val, 1)})

            elevation_trajectories.append({
                "object_name": body,
                "points": hourly_points,
            })

        # 3. Solar & Twilight Telemetry
        solar = self._engine.get_solar_summary(context)
        astro_begin = solar.astronomical_twilight_begin.isoformat() if solar.astronomical_twilight_begin else None
        astro_end = solar.astronomical_twilight_end.isoformat() if solar.astronomical_twilight_end else None

        # Calculate dark sky duration in hours if available
        dark_hours = 8.0
        if solar.astronomical_twilight_end and solar.astronomical_twilight_begin:
            diff = (solar.astronomical_twilight_begin - solar.astronomical_twilight_end).total_seconds() / 3600.0
            if diff > 0:
                dark_hours = round(diff, 1)

        # 4. Database Catalog Telemetry
        total_events = 0
        total_apods = 0
        if db_session is not None:
            try:
                total_events = db_session.query(CelestialEvent).count()
                total_apods = db_session.query(NasaApod).count()
            except Exception:
                pass

        return {
            "timestamp": ts.isoformat(),
            "location": {
                "latitude": latitude,
                "longitude": longitude,
            },
            "target_scores": scores,
            "category_distribution": category_counts,
            "elevation_trajectories": elevation_trajectories,
            "telemetry": {
                "dark_hours": dark_hours,
                "astronomical_twilight_begin": astro_begin,
                "astronomical_twilight_end": astro_end,
                "total_events_cataloged": total_events,
                "total_apod_entries": total_apods,
                "visible_target_count": sum(1 for s in scores if s["is_visible"]),
            },
        }
