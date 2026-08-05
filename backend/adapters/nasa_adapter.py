"""NASA API adapter for the backend service layer.

All external NASA API calls are isolated here. The frontend and other backend
modules access NASA data only through this adapter or via the database.
"""

from __future__ import annotations

import os
import logging
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NasaApiConfig:
    """Configuration for NASA API access."""

    api_key: str = field(default_factory=lambda: os.getenv("NASA_API_KEY", "DEMO_KEY"))
    base_url: str = "https://api.nasa.gov"
    timeout_seconds: int = 15


@dataclass(frozen=True)
class ApodResult:
    """Structured result from the NASA APOD API."""

    apod_date: str
    title: str
    explanation: Optional[str] = None
    url: Optional[str] = None
    hdurl: Optional[str] = None
    media_type: Optional[str] = None
    copyright_text: Optional[str] = None
    thumbnail_url: Optional[str] = None


class NasaApiError(RuntimeError):
    """Raised when a NASA API request fails."""


class NasaAdapter:
    """Adapter for interacting with NASA public APIs.

    Designed to be extensible — additional NASA API methods (NEO, EPIC, etc.)
    can be added without changing the adapter interface.
    """

    def __init__(self, config: Optional[NasaApiConfig] = None) -> None:
        self._config = config or NasaApiConfig()

    def get_apod(self, target_date: Optional[date] = None) -> ApodResult:
        """Fetch the Astronomy Picture of the Day for a given date."""
        params: Dict[str, Any] = {"api_key": self._config.api_key}
        if target_date is not None:
            params["date"] = target_date.isoformat()

        try:
            response = requests.get(
                f"{self._config.base_url}/planetary/apod",
                params=params,
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("NASA APOD API request failed: %s", exc)
            raise NasaApiError(f"Failed to fetch APOD: {exc}") from exc

        data = response.json()
        return ApodResult(
            apod_date=data.get("date", ""),
            title=data.get("title", ""),
            explanation=data.get("explanation"),
            url=data.get("url"),
            hdurl=data.get("hdurl"),
            media_type=data.get("media_type"),
            copyright_text=data.get("copyright"),
            thumbnail_url=data.get("thumbnail_url"),
        )

    def get_apod_range(
        self, start_date: date, end_date: Optional[date] = None
    ) -> List[ApodResult]:
        """Fetch APOD entries for a date range."""
        params: Dict[str, Any] = {
            "api_key": self._config.api_key,
            "start_date": start_date.isoformat(),
        }
        if end_date is not None:
            params["end_date"] = end_date.isoformat()

        try:
            response = requests.get(
                f"{self._config.base_url}/planetary/apod",
                params=params,
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error("NASA APOD range request failed: %s", exc)
            raise NasaApiError(f"Failed to fetch APOD range: {exc}") from exc

        entries = response.json()
        if isinstance(entries, dict):
            entries = [entries]

        return [
            ApodResult(
                apod_date=entry.get("date", ""),
                title=entry.get("title", ""),
                explanation=entry.get("explanation"),
                url=entry.get("url"),
                hdurl=entry.get("hdurl"),
                media_type=entry.get("media_type"),
                copyright_text=entry.get("copyright"),
                thumbnail_url=entry.get("thumbnail_url"),
            )
            for entry in entries
        ]
