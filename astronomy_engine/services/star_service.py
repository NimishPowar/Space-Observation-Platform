"""Star service for calculating positions and visibility of bright stars."""

from __future__ import annotations

from abc import ABC, abstractmethod
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional

from astronomy_engine.core.domain import ObservationContext, StarPosition


# Catalog of 40 prominent bright stars in the night sky
BRIGHT_STARS_CATALOG: List[Dict[str, object]] = [
    {"name": "Sirius", "bayer": "Alpha Canis Majoris", "constellation": "Canis Major", "ra": 6.752, "dec": -16.716, "mag": -1.46, "spectral": "A1V", "color": "#d5e0ff"},
    {"name": "Canopus", "bayer": "Alpha Carinae", "constellation": "Carina", "ra": 6.399, "dec": -52.697, "mag": -0.74, "spectral": "A9II", "color": "#f8f7ff"},
    {"name": "Rigel Kentaurus", "bayer": "Alpha Centauri A", "constellation": "Centaurus", "ra": 14.659, "dec": -60.835, "mag": -0.01, "spectral": "G2V", "color": "#ffea79"},
    {"name": "Arcturus", "bayer": "Alpha Boötis", "constellation": "Boötes", "ra": 14.261, "dec": 19.182, "mag": -0.05, "spectral": "K1.5III", "color": "#ffb366"},
    {"name": "Vega", "bayer": "Alpha Lyrae", "constellation": "Lyra", "ra": 18.616, "dec": 38.784, "mag": 0.03, "spectral": "A0V", "color": "#8cb4ff"},
    {"name": "Capella", "bayer": "Alpha Aurigae", "constellation": "Auriga", "ra": 5.278, "dec": 45.998, "mag": 0.08, "spectral": "G3III", "color": "#ffea79"},
    {"name": "Rigel", "bayer": "Beta Orionis", "constellation": "Orion", "ra": 5.242, "dec": -8.202, "mag": 0.13, "spectral": "B8Ia", "color": "#8cb4ff"},
    {"name": "Procyon", "bayer": "Alpha Canis Minoris", "constellation": "Canis Minor", "ra": 7.655, "dec": 5.225, "mag": 0.37, "spectral": "F5IV-V", "color": "#f8f7ff"},
    {"name": "Betelgeuse", "bayer": "Alpha Orionis", "constellation": "Orion", "ra": 5.919, "dec": 7.407, "mag": 0.50, "spectral": "M1-M2Ia-ab", "color": "#ff7066"},
    {"name": "Achernar", "bayer": "Alpha Eridani", "constellation": "Eridanus", "ra": 1.629, "dec": -57.237, "mag": 0.46, "spectral": "B6Vep", "color": "#8cb4ff"},
    {"name": "Hadar", "bayer": "Beta Centauri", "constellation": "Centaurus", "ra": 14.064, "dec": -60.373, "mag": 0.61, "spectral": "B1III", "color": "#8cb4ff"},
    {"name": "Altair", "bayer": "Alpha Aquilae", "constellation": "Aquila", "ra": 19.846, "dec": 8.868, "mag": 0.76, "spectral": "A7V", "color": "#d5e0ff"},
    {"name": "Acrux", "bayer": "Alpha Crucis", "constellation": "Crux", "ra": 12.443, "dec": -63.099, "mag": 0.76, "spectral": "B0.5IV", "color": "#8cb4ff"},
    {"name": "Aldebaran", "bayer": "Alpha Tauri", "constellation": "Taurus", "ra": 4.599, "dec": 16.509, "mag": 0.85, "spectral": "K5III", "color": "#ffb366"},
    {"name": "Antares", "bayer": "Alpha Scorpii", "constellation": "Scorpius", "ra": 16.490, "dec": -26.432, "mag": 0.96, "spectral": "M1.5Iab-b", "color": "#ff7066"},
    {"name": "Spica", "bayer": "Alpha Virginis", "constellation": "Virgo", "ra": 13.420, "dec": -11.161, "mag": 0.97, "spectral": "B1III-IV", "color": "#8cb4ff"},
    {"name": "Pollux", "bayer": "Beta Geminorum", "constellation": "Gemini", "ra": 7.755, "dec": 28.026, "mag": 1.14, "spectral": "K0III", "color": "#ffb366"},
    {"name": "Fomalhaut", "bayer": "Alpha Piscis Austrini", "constellation": "Piscis Austrinus", "ra": 22.961, "dec": -29.622, "mag": 1.16, "spectral": "A3V", "color": "#d5e0ff"},
    {"name": "Deneb", "bayer": "Alpha Cygni", "constellation": "Cygnus", "ra": 20.690, "dec": 45.280, "mag": 1.25, "spectral": "A2Ia", "color": "#d5e0ff"},
    {"name": "Mimosa", "bayer": "Beta Crucis", "constellation": "Crux", "ra": 12.795, "dec": -59.689, "mag": 1.25, "spectral": "B0.5III", "color": "#8cb4ff"},
    {"name": "Regulus", "bayer": "Alpha Leonis", "constellation": "Leo", "ra": 10.140, "dec": 11.967, "mag": 1.36, "spectral": "B8IVn", "color": "#8cb4ff"},
    {"name": "Adhara", "bayer": "Epsilon Canis Majoris", "constellation": "Canis Major", "ra": 6.977, "dec": -28.972, "mag": 1.50, "spectral": "B1.5II", "color": "#8cb4ff"},
    {"name": "Castor", "bayer": "Alpha Geminorum", "constellation": "Gemini", "ra": 7.577, "dec": 31.888, "mag": 1.58, "spectral": "A1V", "color": "#d5e0ff"},
    {"name": "Gacrux", "bayer": "Gamma Crucis", "constellation": "Crux", "ra": 12.519, "dec": -57.113, "mag": 1.64, "spectral": "M3.5III", "color": "#ff7066"},
    {"name": "Bellatrix", "bayer": "Gamma Orionis", "constellation": "Orion", "ra": 5.420, "dec": 6.350, "mag": 1.64, "spectral": "B2III", "color": "#8cb4ff"},
    {"name": "Elnath", "bayer": "Beta Tauri", "constellation": "Taurus", "ra": 5.438, "dec": 28.608, "mag": 1.65, "spectral": "B7III", "color": "#8cb4ff"},
    {"name": "Alnilam", "bayer": "Epsilon Orionis", "constellation": "Orion", "ra": 5.604, "dec": -1.202, "mag": 1.69, "spectral": "B0Ia", "color": "#8cb4ff"},
    {"name": "Alnitak", "bayer": "Zeta Orionis", "constellation": "Orion", "ra": 5.679, "dec": -1.942, "mag": 1.77, "spectral": "O9.7Ib", "color": "#8cb4ff"},
    {"name": "Saiph", "bayer": "Kappa Orionis", "constellation": "Orion", "ra": 5.796, "dec": -9.670, "mag": 2.07, "spectral": "B0.5Ia", "color": "#8cb4ff"},
    {"name": "Polaris", "bayer": "Alpha Ursae Minoris", "constellation": "Ursa Minor", "ra": 2.530, "dec": 89.264, "mag": 1.98, "spectral": "F7Ib", "color": "#f8f7ff"},
    {"name": "Dubhe", "bayer": "Alpha Ursae Majoris", "constellation": "Ursa Major", "ra": 11.062, "dec": 61.751, "mag": 1.79, "spectral": "K0III", "color": "#ffb366"},
    {"name": "Merak", "bayer": "Beta Ursae Majoris", "constellation": "Ursa Major", "ra": 11.031, "dec": 56.382, "mag": 2.37, "spectral": "A1V", "color": "#d5e0ff"},
    {"name": "Phecda", "bayer": "Gamma Ursae Majoris", "constellation": "Ursa Major", "ra": 11.900, "dec": 53.695, "mag": 2.44, "spectral": "A0Ve", "color": "#d5e0ff"},
    {"name": "Megrez", "bayer": "Delta Ursae Majoris", "constellation": "Ursa Major", "ra": 12.257, "dec": 57.032, "mag": 3.31, "spectral": "A3V", "color": "#d5e0ff"},
    {"name": "Alioth", "bayer": "Epsilon Ursae Majoris", "constellation": "Ursa Major", "ra": 12.900, "dec": 55.960, "mag": 1.77, "spectral": "A1p", "color": "#d5e0ff"},
    {"name": "Mizar", "bayer": "Zeta Ursae Majoris", "constellation": "Ursa Major", "ra": 13.399, "dec": 54.925, "mag": 2.23, "spectral": "A2V", "color": "#d5e0ff"},
    {"name": "Alkaid", "bayer": "Eta Ursae Majoris", "constellation": "Ursa Major", "ra": 13.792, "dec": 49.313, "mag": 1.85, "spectral": "B3V", "color": "#8cb4ff"},
    {"name": "Schedar", "bayer": "Alpha Cassiopeiae", "constellation": "Cassiopeia", "ra": 0.675, "dec": 56.537, "mag": 2.24, "spectral": "K0IIIa", "color": "#ffb366"},
    {"name": "Caph", "bayer": "Beta Cassiopeiae", "constellation": "Cassiopeia", "ra": 0.153, "dec": 59.150, "mag": 2.28, "spectral": "F2III", "color": "#f8f7ff"},
    {"name": "Gamma Cassiopeiae", "bayer": "Gamma Cassiopeiae", "constellation": "Cassiopeia", "ra": 0.945, "dec": 60.717, "mag": 2.15, "spectral": "B0IVe", "color": "#8cb4ff"},
]


def calculate_star_altaz(
    ra_hours: float,
    dec_deg: float,
    lat_deg: float,
    lon_deg: float,
    dt: datetime,
) -> tuple[float, float]:
    """Calculate Altitude and Azimuth for a star given observer coordinates and datetime."""
    utc_dt = dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    y, m, d = utc_dt.year, utc_dt.month, utc_dt.day
    h, mins, s = utc_dt.hour, utc_dt.minute, utc_dt.second

    if m <= 2:
        y -= 1
        m += 12
    a = math.floor(y / 100.0)
    b = 2 - a + math.floor(a / 4.0)
    jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5 + (h + mins / 60.0 + s / 3600.0) / 24.0
    day_offset = jd - 2451545.0

    gmst = (280.46061837 + 360.98564736629 * day_offset) % 360.0
    lst = (gmst + lon_deg) % 360.0
    ha = (lst - ra_hours * 15.0) % 360.0

    phi_rad = math.radians(lat_deg)
    dec_rad = math.radians(dec_deg)
    ha_rad = math.radians(ha)

    sin_alt = math.sin(phi_rad) * math.sin(dec_rad) + math.cos(phi_rad) * math.cos(dec_rad) * math.cos(ha_rad)
    sin_alt = max(-1.0, min(1.0, sin_alt))
    alt_deg = math.degrees(math.asin(sin_alt))

    y_az = -math.cos(dec_rad) * math.sin(ha_rad)
    x_az = math.sin(dec_rad) - math.sin(phi_rad) * sin_alt
    az_deg = math.degrees(math.atan2(y_az, x_az)) % 360.0

    return alt_deg, az_deg


class StarService(ABC):
    """Abstract base class for star calculation service."""

    @abstractmethod
    def list_visible_stars(
        self,
        context: ObservationContext,
        min_altitude: float = 0.0,
    ) -> List[StarPosition]:
        """Return visible star positions for the given observation context."""
        pass


class DefaultStarService(StarService):
    """Concrete implementation of StarService evaluating catalog positions."""

    def __init__(self, catalog: Optional[List[Dict[str, object]]] = None) -> None:
        self._catalog = catalog or BRIGHT_STARS_CATALOG

    def list_visible_stars(
        self,
        context: ObservationContext,
        min_altitude: float = 0.0,
    ) -> List[StarPosition]:
        stars: List[StarPosition] = []
        lat = context.location.latitude
        lon = context.location.longitude
        dt = context.timestamp

        for entry in self._catalog:
            alt, az = calculate_star_altaz(
                ra_hours=float(entry["ra"]),
                dec_deg=float(entry["dec"]),
                lat_deg=lat,
                lon_deg=lon,
                dt=dt,
            )
            is_vis = alt >= min_altitude
            star = StarPosition(
                name=str(entry["name"]),
                bayer_designation=str(entry["bayer"]),
                constellation=str(entry["constellation"]),
                right_ascension=float(entry["ra"]),
                declination=float(entry["dec"]),
                azimuth=round(az, 2),
                altitude=round(alt, 2),
                magnitude=float(entry["mag"]),
                spectral_type=str(entry["spectral"]),
                color_hex=str(entry["color"]),
                is_visible=is_vis,
            )
            if is_vis:
                stars.append(star)

        # Sort by visual brightness (lowest magnitude first)
        stars.sort(key=lambda s: s.magnitude if s.magnitude is not None else 99.0)
        return stars
