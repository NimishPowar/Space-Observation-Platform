"""Pydantic response models for backend API endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class MoonResponse(BaseModel):
    phase_name: str
    illumination: float
    phase_angle: float
    age_days: Optional[float] = None
    distance_km: Optional[float] = None
    prev_phase_name: Optional[str] = None
    prev_phase_date: Optional[datetime] = None
    next_phase_name: Optional[str] = None
    next_phase_date: Optional[datetime] = None


class MoonSimulatorResponse(MoonResponse):
    rise_time: Optional[datetime] = None
    set_time: Optional[datetime] = None
    unicode_symbol: Optional[str] = None


class PlanetPositionResponse(BaseModel):
    object_name: str
    right_ascension: float
    declination: float
    azimuth: Optional[float] = None
    altitude: Optional[float] = None
    distance_au: Optional[float] = None
    magnitude: Optional[float] = None
    is_visible: Optional[bool] = None


class VisibilityWindowResponse(BaseModel):
    object_name: str
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    max_elevation: Optional[float] = None
    azimuth_at_max: Optional[float] = None
    score: Optional[float] = None
    description: Optional[str] = None


class ObservationScoreResponse(BaseModel):
    object_name: str
    score: float
    score_reason: Optional[str] = None
    visibility_window: Optional[VisibilityWindowResponse] = None
    metrics: Optional[dict] = None


class SolarStateResponse(BaseModel):
    sunrise: Optional[datetime] = None
    sunset: Optional[datetime] = None
    solar_noon: Optional[datetime] = None
    day_length_minutes: Optional[float] = None
    elevation: Optional[float] = None
    azimuth: Optional[float] = None
    civil_twilight_begin: Optional[datetime] = None
    civil_twilight_end: Optional[datetime] = None
    nautical_twilight_begin: Optional[datetime] = None
    nautical_twilight_end: Optional[datetime] = None
    astronomical_twilight_begin: Optional[datetime] = None
    astronomical_twilight_end: Optional[datetime] = None


class CelestialEventResponse(BaseModel):
    event_id: Optional[str] = None
    name: str
    category: str
    event_type: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    visible_objects: Optional[List[str]] = None
    magnitude: Optional[float] = None
    location: Optional[dict] = None


class LearnResponse(BaseModel):
    object_name: str
    slug: str
    title: str
    excerpt: Optional[str] = None
    body: Optional[str] = None
    category_slug: str
    category_name: str
    source_url: Optional[str] = None
    is_featured: bool


class DiscoveryCategoryResponse(BaseModel):
    slug: str
    name: str
    description: Optional[str] = None


class DiscoveryTopicResponse(LearnResponse):
    pass


class StarResponse(BaseModel):
    name: str
    bayer_designation: str
    constellation: str
    right_ascension: float
    declination: float
    azimuth: Optional[float] = None
    altitude: Optional[float] = None
    magnitude: Optional[float] = None
    spectral_type: Optional[str] = None
    color_hex: Optional[str] = None
    is_visible: Optional[bool] = None


class ConstellationResponse(BaseModel):
    name: str
    latin_name: str
    abbreviation: str
    center_azimuth: Optional[float] = None
    center_altitude: Optional[float] = None
    star_names: Optional[List[str]] = None
    lines: Optional[List[List[str]]] = None
    is_visible: Optional[bool] = None


class SkyMapResponse(BaseModel):
    timestamp: datetime
    location: Optional[dict] = None
    moon: Optional[MoonResponse] = None
    sun: Optional[SolarStateResponse] = None
    planets: List[PlanetPositionResponse] = []
    stars: List[StarResponse] = []
    constellations: List[ConstellationResponse] = []

