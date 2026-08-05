"""Domain models for the astronomy engine.

These models define the boundary objects used by engine services and keep the
astronomical domain independent from web and UI frameworks.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Location:
    """Observer location used for astronomy calculations."""

    latitude: float
    longitude: float
    elevation_meters: Optional[float] = None
    name: Optional[str] = None


@dataclass(frozen=True)
class ObservationContext:
    """Context that describes when and where to evaluate astronomy data."""

    location: Location
    timestamp: datetime
    timezone: Optional[str] = None
    target_objects: Optional[List[str]] = None


@dataclass(frozen=True)
class MoonPhase:
    """Moon phase information and illumination state."""

    phase_name: str
    illumination: float
    phase_angle: float
    age_days: Optional[float] = None
    distance_km: Optional[float] = None


@dataclass(frozen=True)
class MoonVisibility:
    """Lunar visibility metrics for a specific observer context."""

    rise_time: Optional[datetime]
    set_time: Optional[datetime]
    transit_time: Optional[datetime] = None
    altitude_at_transit: Optional[float] = None
    azimuth_rise: Optional[float] = None
    azimuth_set: Optional[float] = None
    is_visible: Optional[bool] = None


@dataclass(frozen=True)
class PlanetPosition:
    """Astronomical position and visibility state for a planet."""

    object_name: str
    right_ascension: float
    declination: float
    azimuth: Optional[float] = None
    altitude: Optional[float] = None
    distance_au: Optional[float] = None
    magnitude: Optional[float] = None
    is_visible: Optional[bool] = None


@dataclass(frozen=True)
class SolarState:
    """Solar timing and state information for a given observer context."""

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


@dataclass(frozen=True)
class VisibilityWindow:
    """A time interval when a celestial object is observable."""

    object_name: str
    start: datetime
    end: datetime
    max_elevation: Optional[float] = None
    azimuth_at_max: Optional[float] = None
    score: Optional[float] = None
    description: Optional[str] = None


@dataclass(frozen=True)
class ObservationScore:
    """Score and reasoning to rank observation opportunities."""

    object_name: str
    score: float
    score_reason: Optional[str] = None
    visibility_window: Optional[VisibilityWindow] = None
    metrics: Optional[Dict[str, float]] = None


@dataclass(frozen=True)
class CelestialEvent:
    """Metadata for a named celestial event."""

    name: str
    category: str
    start_time: datetime
    end_time: Optional[datetime] = None
    event_type: Optional[str] = None
    description: Optional[str] = None
    visibility_window: Optional[VisibilityWindow] = None
    visible_objects: Optional[List[str]] = None
    magnitude: Optional[float] = None
    location: Optional[Location] = None
    event_id: Optional[str] = None


@dataclass(frozen=True)
class StarPosition:
    """Astronomical position and visibility state for a bright star."""

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


@dataclass(frozen=True)
class ConstellationData:
    """Constellation metadata and star line connections."""

    name: str
    latin_name: str
    abbreviation: str
    center_azimuth: Optional[float] = None
    center_altitude: Optional[float] = None
    star_names: Optional[List[str]] = None
    lines: Optional[List[List[str]]] = None
    is_visible: Optional[bool] = None


@dataclass(frozen=True)
class SkyMapData:
    """Aggregated sky map domain model for rendering the night sky."""

    timestamp: datetime
    location: Location
    moon: Optional[MoonPhase] = None
    sun: Optional[SolarState] = None
    planets: List[PlanetPosition] = field(default_factory=list)
    stars: List[StarPosition] = field(default_factory=list)
    constellations: List[ConstellationData] = field(default_factory=list)

