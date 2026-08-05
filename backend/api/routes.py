"""API routes for astronomy endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query, Depends

from astronomy_engine.core.domain import Location, ObservationContext
from backend.schemas.apod_models import ApodResponse
from backend.use_cases.astronomy_use_case import AstronomyUseCase
from backend.schemas.models import (
    MoonResponse,
    PlanetPositionResponse,
    VisibilityWindowResponse,
    ObservationScoreResponse,
    CelestialEventResponse,
    SolarStateResponse,
    LearnResponse,
    StarResponse,
    ConstellationResponse,
    SkyMapResponse,
)
from backend.api.dependencies import (
    get_astronomy_use_case,
    get_events_use_case,
    get_learn_use_case,
    get_nasa_apod_use_case,
    get_observation_planner_use_case,
)
from backend.use_cases.events_use_case import EventsUseCase
from backend.use_cases.learn_use_case import LearnUseCase
from backend.use_cases.nasa_apod_use_case import NasaApodUseCase
from backend.use_cases.observation_planner import ObservationPlannerUseCase

router = APIRouter()


def _parse_timestamp(ts: Optional[str]) -> datetime:
    if ts is None:
        return datetime.now(timezone.utc)
    try:
        dt = datetime.fromisoformat(ts)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid timestamp: {exc}")


def _build_context(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    targets: Optional[List[str]] = None,
) -> ObservationContext:
    location = Location(latitude=latitude, longitude=longitude, elevation_meters=elevation)
    ts = _parse_timestamp(timestamp)
    return ObservationContext(location=location, timestamp=ts, timezone=str(ts.tzinfo), target_objects=targets)


def _serialize(obj: Any) -> Any:
    """Serialize domain models to JSON-friendly structures."""
    from dataclasses import is_dataclass, asdict

    if obj is None:
        return None
    if is_dataclass(obj):
        d = asdict(obj)
        for k, v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
            elif is_dataclass(v) or isinstance(v, (list, dict)):
                d[k] = _serialize(v)
        return d
    if isinstance(obj, list):
        return [_serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


@router.get("/moon", response_model=MoonResponse)
def get_moon(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation)
    moon = use_case.get_moon_summary(context)
    return _serialize(moon)


@router.get("/planets", response_model=List[PlanetPositionResponse])
def get_planets(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    names: Optional[List[str]] = Query(None),
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation, names)
    planets = use_case.get_planetary_positions(context)
    return _serialize(planets)


@router.get("/stars", response_model=List[StarResponse])
def get_stars(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    min_altitude: float = Query(0.0),
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation)
    stars = use_case.get_star_positions(context, min_altitude=min_altitude)
    return _serialize(stars)


@router.get("/constellations", response_model=List[ConstellationResponse])
def get_constellations(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation)
    constellations = use_case.get_constellations(context)
    return _serialize(constellations)


@router.get("/skymap", response_model=SkyMapResponse)
def get_skymap(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation)
    skymap_data = use_case.get_skymap_data(context)
    return _serialize(skymap_data)


@router.get("/visibility", response_model=List[VisibilityWindowResponse])
def get_visibility(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    names: Optional[List[str]] = Query(None),
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation, names)
    windows = use_case.get_visibility_windows(context, names)
    return _serialize(windows)


@router.get("/planner", response_model=List[ObservationScoreResponse])
def get_planner(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    names: Optional[List[str]] = Query(None),
    limit: int = Query(5, ge=1, le=10),
    use_case: ObservationPlannerUseCase = Depends(get_observation_planner_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation, names)
    scores = use_case.estimate_window(context, names, limit=limit)
    return _serialize(scores)


@router.get("/sun", response_model=SolarStateResponse)
def get_sun(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    elevation: Optional[float] = None,
    use_case: AstronomyUseCase = Depends(get_astronomy_use_case),
):
    context = _build_context(latitude, longitude, timestamp, elevation)
    solar = use_case.get_solar_summary(context)
    return _serialize(solar)


@router.get("/events", response_model=List[CelestialEventResponse])
def get_events(
    latitude: float,
    longitude: float,
    timestamp: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    use_case: EventsUseCase = Depends(get_events_use_case),
):
    ts = _parse_timestamp(timestamp)
    events = use_case.list_upcoming_events(from_time=ts, limit=limit)
    return [_serialize(event) for event in events]


@router.get("/learn/{object_name}", response_model=LearnResponse)
def get_learn(
    object_name: str,
    use_case: LearnUseCase = Depends(get_learn_use_case),
):
    content = use_case.get_content_for_object(object_name)
    if content is None:
        raise HTTPException(
            status_code=404,
            detail=f"No educational content found for '{object_name}'",
        )
    return _serialize(content)


@router.get("/apod/today", response_model=ApodResponse)
def get_apod_today(
    use_case: NasaApodUseCase = Depends(get_nasa_apod_use_case),
):
    apod = use_case.get_today()
    if apod is None:
        raise HTTPException(
            status_code=404,
            detail="No APOD entry found for today in the platform catalog.",
        )
    return _serialize(apod)


@router.get("/apod/recent", response_model=List[ApodResponse])
def get_apod_recent(
    limit: int = Query(10, ge=1, le=50),
    use_case: NasaApodUseCase = Depends(get_nasa_apod_use_case),
):
    apods = use_case.get_recent(limit=limit)
    return [_serialize(a) for a in apods]


@router.get("/apod/{target_date}", response_model=ApodResponse)
def get_apod_by_date(
    target_date: str,
    use_case: NasaApodUseCase = Depends(get_nasa_apod_use_case),
):
    apod = use_case.get_by_date(target_date)
    if apod is None:
        raise HTTPException(
            status_code=404,
            detail=f"No APOD entry found for date '{target_date}'.",
        )
    return _serialize(apod)

