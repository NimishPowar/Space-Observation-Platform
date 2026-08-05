"""Constellation service for computing constellation visibility and star connections."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from astronomy_engine.core.domain import ConstellationData, ObservationContext, StarPosition
from astronomy_engine.services.star_service import DefaultStarService, StarService


CONSTELLATIONS_CATALOG: List[Dict[str, object]] = [
    {
        "name": "Orion",
        "latin": "Orion",
        "abbrev": "Ori",
        "stars": ["Betelgeuse", "Rigel", "Bellatrix", "Saiph", "Alnitak", "Alnilam"],
        "lines": [
            ["Betelgeuse", "Bellatrix"],
            ["Betelgeuse", "Alnitak"],
            ["Bellatrix", "Alnilam"],
            ["Alnitak", "Alnilam"],
            ["Alnilam", "Saiph"],
            ["Alnitak", "Saiph"],
            ["Saiph", "Rigel"],
            ["Rigel", "Bellatrix"],
        ],
    },
    {
        "name": "Ursa Major (Big Dipper)",
        "latin": "Ursa Major",
        "abbrev": "UMa",
        "stars": ["Dubhe", "Merak", "Phecda", "Megrez", "Alioth", "Mizar", "Alkaid"],
        "lines": [
            ["Dubhe", "Merak"],
            ["Merak", "Phecda"],
            ["Phecda", "Megrez"],
            ["Megrez", "Dubhe"],
            ["Megrez", "Alioth"],
            ["Alioth", "Mizar"],
            ["Mizar", "Alkaid"],
        ],
    },
    {
        "name": "Cassiopeia",
        "latin": "Cassiopeia",
        "abbrev": "Cas",
        "stars": ["Caph", "Schedar", "Gamma Cassiopeiae"],
        "lines": [
            ["Caph", "Schedar"],
            ["Schedar", "Gamma Cassiopeiae"],
        ],
    },
    {
        "name": "Canis Major",
        "latin": "Canis Major",
        "abbrev": "CMa",
        "stars": ["Sirius", "Adhara"],
        "lines": [
            ["Sirius", "Adhara"],
        ],
    },
    {
        "name": "Crux (Southern Cross)",
        "latin": "Crux",
        "abbrev": "Cru",
        "stars": ["Acrux", "Mimosa", "Gacrux"],
        "lines": [
            ["Acrux", "Gacrux"],
            ["Mimosa", "Acrux"],
        ],
    },
    {
        "name": "Gemini",
        "latin": "Gemini",
        "abbrev": "Gem",
        "stars": ["Castor", "Pollux"],
        "lines": [
            ["Castor", "Pollux"],
        ],
    },
    {
        "name": "Centaurus",
        "latin": "Centaurus",
        "abbrev": "Cen",
        "stars": ["Rigel Kentaurus", "Hadar"],
        "lines": [
            ["Rigel Kentaurus", "Hadar"],
        ],
    },
]


class ConstellationService(ABC):
    """Abstract base class for constellation service."""

    @abstractmethod
    def list_constellations(
        self,
        context: ObservationContext,
        star_positions: Optional[List[StarPosition]] = None,
    ) -> List[ConstellationData]:
        """Return constellation visibility and line mappings for context."""
        pass


class DefaultConstellationService(ConstellationService):
    """Default implementation of ConstellationService."""

    def __init__(
        self,
        catalog: Optional[List[Dict[str, object]]] = None,
        star_service: Optional[StarService] = None,
    ) -> None:
        self._catalog = catalog or CONSTELLATIONS_CATALOG
        self._star_service = star_service or DefaultStarService()

    def list_constellations(
        self,
        context: ObservationContext,
        star_positions: Optional[List[StarPosition]] = None,
    ) -> List[ConstellationData]:
        stars = star_positions if star_positions is not None else self._star_service.list_visible_stars(context, min_altitude=-90.0)
        star_lookup: Dict[str, StarPosition] = {s.name: s for s in stars}

        constellations: List[ConstellationData] = []
        for entry in self._catalog:
            const_name = str(entry["name"])
            star_names = [str(name) for name in entry.get("stars", [])]
            raw_lines = entry.get("lines", [])
            lines: List[List[str]] = [[str(pair[0]), str(pair[1])] for pair in raw_lines]

            # Calculate center altitude/azimuth from star positions
            altitudes = [star_lookup[n].altitude for n in star_names if n in star_lookup and star_lookup[n].altitude is not None]
            azimuths = [star_lookup[n].azimuth for n in star_names if n in star_lookup and star_lookup[n].azimuth is not None]

            avg_alt = sum(altitudes) / len(altitudes) if altitudes else None
            avg_az = sum(azimuths) / len(azimuths) if azimuths else None
            visible_stars_count = sum(1 for n in star_names if n in star_lookup and star_lookup[n].is_visible)

            # Constellation is visible if at least 1 star is visible or center altitude > 0
            is_vis = visible_stars_count > 0 or (avg_alt is not None and avg_alt > 0)

            constellations.append(
                ConstellationData(
                    name=const_name,
                    latin_name=str(entry.get("latin", const_name)),
                    abbreviation=str(entry.get("abbrev", "")),
                    center_azimuth=round(avg_az, 2) if avg_az is not None else None,
                    center_altitude=round(avg_alt, 2) if avg_alt is not None else None,
                    star_names=star_names,
                    lines=lines,
                    is_visible=is_vis,
                )
            )

        return constellations
