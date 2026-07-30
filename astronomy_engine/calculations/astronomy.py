"""Astronomy calculation helpers for the astronomy engine."""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional

from skyfield import almanac
from skyfield.api import Loader, load, wgs84

from astronomy_engine.core.domain import (
    Location,
    MoonPhase,
    MoonVisibility,
    PlanetPosition,
    SolarState,
    VisibilityWindow,
)


SOLAR_SYSTEM_BODIES: Dict[str, str] = {
    "Mercury": "mercury",
    "Venus": "venus",
    "Earth": "earth",
    "Mars": "mars",
    "Jupiter": "jupiter barycenter",
    "Saturn": "saturn barycenter",
    "Uranus": "uranus barycenter",
    "Neptune": "neptune barycenter",
    "Sun": "sun",
    "Moon": "moon",
}


def _get_loader() -> Loader:
    data_dir = Path.home() / ".skyfield"
    data_dir.mkdir(parents=True, exist_ok=True)
    return Loader(str(data_dir))


def load_ephemeris() -> object:
    loader = _get_loader()
    return loader("de421.bsp")


def load_timescale() -> object:
    return load.timescale()


def to_utc_datetime(ts_time) -> datetime:
    dt = ts_time.utc_datetime()
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_time(value: Optional[datetime]) -> Optional[datetime]:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def phase_name_from_angle(phase_degrees: float) -> str:
    value = phase_degrees % 360.0
    if value < 22.5 or value >= 337.5:
        return "New Moon"
    if value < 67.5:
        return "Waxing Crescent"
    if value < 112.5:
        return "First Quarter"
    if value < 157.5:
        return "Waxing Gibbous"
    if value < 202.5:
        return "Full Moon"
    if value < 247.5:
        return "Waning Gibbous"
    if value < 292.5:
        return "Last Quarter"
    return "Waning Crescent"


def make_moon_phase(state: Dict[str, object]) -> MoonPhase:
    return MoonPhase(
        phase_name=state.get("phase_name", "Unknown"),
        illumination=state.get("illumination", 0.0),
        phase_angle=state.get("phase_angle", 0.0),
        age_days=state.get("age_days"),
        distance_km=state.get("distance_km"),
    )


def make_moon_visibility(state: Dict[str, object]) -> MoonVisibility:
    return MoonVisibility(
        rise_time=state.get("rise_time"),
        set_time=state.get("set_time"),
        transit_time=state.get("transit_time"),
        altitude_at_transit=state.get("altitude_at_transit"),
        azimuth_rise=state.get("azimuth_rise"),
        azimuth_set=state.get("azimuth_set"),
        is_visible=state.get("is_visible"),
    )


def make_planet_position(state: Dict[str, object]) -> PlanetPosition:
    return PlanetPosition(
        object_name=state.get("object_name", ""),
        right_ascension=state.get("right_ascension", 0.0),
        declination=state.get("declination", 0.0),
        azimuth=state.get("azimuth"),
        altitude=state.get("altitude"),
        distance_au=state.get("distance_au"),
        magnitude=state.get("magnitude"),
        is_visible=state.get("is_visible"),
    )


def make_solar_state(state: Dict[str, object]) -> SolarState:
    return SolarState(
        sunrise=state.get("sunrise"),
        sunset=state.get("sunset"),
        solar_noon=state.get("solar_noon"),
        day_length_minutes=state.get("day_length_minutes"),
        elevation=state.get("elevation"),
        azimuth=state.get("azimuth"),
        civil_twilight_begin=state.get("civil_twilight_begin"),
        civil_twilight_end=state.get("civil_twilight_end"),
        nautical_twilight_begin=state.get("nautical_twilight_begin"),
        nautical_twilight_end=state.get("nautical_twilight_end"),
        astronomical_twilight_begin=state.get("astronomical_twilight_begin"),
        astronomical_twilight_end=state.get("astronomical_twilight_end"),
    )


def make_visibility_window(object_name: str, state: Dict[str, object]) -> VisibilityWindow:
    return VisibilityWindow(
        object_name=object_name,
        start=state.get("rise_time"),
        end=state.get("set_time"),
        max_elevation=state.get("max_elevation"),
        azimuth_at_max=state.get("azimuth_at_max"),
        score=state.get("score"),
        description=state.get("description"),
    )


def create_topocentric_location(ephemeris, location: Location):
    topocentric = ephemeris["earth"] + wgs84.latlon(
        location.latitude,
        location.longitude,
        elevation_m=location.elevation_meters or 0.0,
    )
    return topocentric


def body_for_name(ephemeris, name: str):
    normalized = name.capitalize()
    body_key = SOLAR_SYSTEM_BODIES.get(normalized)
    if body_key is None:
        raise ValueError(f"Unsupported celestial body: {name}")
    return ephemeris[body_key]


def build_time_range(timestamp: datetime):
    utc = timestamp.astimezone(timezone.utc) if timestamp.tzinfo else timestamp.replace(tzinfo=timezone.utc)
    midnight = datetime(utc.year, utc.month, utc.day, tzinfo=timezone.utc)
    return midnight, midnight + timedelta(days=1)


def elevation_and_azimuth(observer, body, ts_time):
    astrometric = observer.at(ts_time).observe(body).apparent()
    alt, az, _ = astrometric.altaz()
    ra, dec, _ = astrometric.radec()
    distance_au = astrometric.distance().au
    return {
        "azimuth": az.degrees,
        "altitude": alt.degrees,
        "right_ascension": ra.hours * 15.0,
        "declination": dec.degrees,
        "distance_au": distance_au,
    }


def calculate_moon_state(ephemeris, ts, observer, timestamp: datetime) -> Dict[str, object]:
    t = ts.utc(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    moon = body_for_name(ephemeris, "Moon")
    phase_angle = float(almanac.moon_phase(ephemeris, t).degrees)
    illumination = (1.0 + math.cos(math.radians(phase_angle))) / 2.0
    state = elevation_and_azimuth(observer, moon, t)
    state.update(
        phase_name=phase_name_from_angle(phase_angle),
        illumination=illumination,
        phase_angle=phase_angle,
        age_days=None,
        distance_km=None,
        object_name="Moon",
    )
    return state


def calculate_solar_state(ephemeris, ts, observer, timestamp: datetime) -> Dict[str, object]:
    t = ts.utc(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    sun = body_for_name(ephemeris, "Sun")
    sun_state = elevation_and_azimuth(observer, sun, t)
    sunrise, sunset = None, None
    try:
        t0, t1 = build_time_range(timestamp)
        times, events = almanac.find_discrete(
            ts.utc(t0.year, t0.month, t0.day, 0, 0, 0),
            ts.utc(t1.year, t1.month, t1.day, 0, 0, 0),
            almanac.sunrise_sunset(ephemeris, observer),
        )
        for time, event in zip(times, events):
            if event == 1 and sunrise is None:
                sunrise = to_utc_datetime(time)
            elif event == 0 and sunset is None:
                sunset = to_utc_datetime(time)
    except Exception:
        sunrise = None
        sunset = None

    state = {
        "sunrise": sunrise,
        "sunset": sunset,
        "solar_noon": None,
        "day_length_minutes": None,
        "elevation": sun_state.get("altitude"),
        "azimuth": sun_state.get("azimuth"),
        "civil_twilight_begin": None,
        "civil_twilight_end": None,
        "nautical_twilight_begin": None,
        "nautical_twilight_end": None,
        "astronomical_twilight_begin": None,
        "astronomical_twilight_end": None,
    }
    return state


def calculate_planet_state(ephemeris, ts, observer, name: str, timestamp: datetime) -> Dict[str, object]:
    t = ts.utc(timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    body = body_for_name(ephemeris, name)
    values = elevation_and_azimuth(observer, body, t)
    values["object_name"] = name
    values["magnitude"] = None
    values["is_visible"] = values["altitude"] >= 0.0
    return values


def calculate_rise_set(ephemeris, ts, observer, body_name: str, timestamp: datetime) -> Dict[str, object]:
    body = body_for_name(ephemeris, body_name)
    t0, t1 = build_time_range(timestamp)
    try:
        times, events = almanac.find_discrete(
            ts.utc(t0.year, t0.month, t0.day, 0, 0, 0),
            ts.utc(t1.year, t1.month, t1.day, 0, 0, 0),
            almanac.risings_and_settings(ephemeris, body, observer),
        )
    except Exception:
        return {
            "rise_time": None,
            "set_time": None,
            "transit_time": None,
            "altitude_at_transit": None,
            "azimuth_rise": None,
            "azimuth_set": None,
            "is_visible": None,
        }

    rise_time = None
    set_time = None
    for time, event in zip(times, events):
        if event == 1 and rise_time is None:
            rise_time = to_utc_datetime(time)
        elif event == 0 and set_time is None:
            set_time = to_utc_datetime(time)
    return {
        "rise_time": rise_time,
        "set_time": set_time,
        "transit_time": None,
        "altitude_at_transit": None,
        "azimuth_rise": None,
        "azimuth_set": None,
        "is_visible": rise_time is not None and set_time is not None,
    }


def list_visible_planets(ephemeris, ts, observer, timestamp: datetime, names: Optional[List[str]] = None) -> List[str]:
    candidates = names or ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    visible: List[str] = []
    for name in candidates:
        state = calculate_planet_state(ephemeris, ts, observer, name, timestamp)
        if state["is_visible"]:
            visible.append(name)
    return visible


def create_visibility_window_from_state(name: str, state: Dict[str, object]) -> VisibilityWindow:
    return VisibilityWindow(
        object_name=name,
        start=state.get("rise_time"),
        end=state.get("set_time"),
        max_elevation=None,
        azimuth_at_max=None,
        score=None,
        description=None,
    )
