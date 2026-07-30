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
