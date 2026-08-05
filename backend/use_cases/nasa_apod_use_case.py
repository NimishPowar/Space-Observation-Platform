"""Use case for NASA APOD data access and management."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional

from database.models import NasaApod
from database.repository import NasaApodRepository


@dataclass(frozen=True)
class ApodEntry:
    """APOD entry result for API responses."""

    apod_date: str
    title: str
    explanation: Optional[str] = None
    url: Optional[str] = None
    hdurl: Optional[str] = None
    media_type: Optional[str] = None
    copyright_text: Optional[str] = None
    thumbnail_url: Optional[str] = None


class NasaApodUseCase:
    """Retrieve NASA APOD data from the local database.

    The frontend calls this use case (via API routes) instead of calling
    the NASA API directly. Data is populated by the ETL pipeline.
    """

    def __init__(self, apod_repository: NasaApodRepository) -> None:
        self._repo = apod_repository

    def get_today(self) -> Optional[ApodEntry]:
        """Return today's APOD entry from the database."""
        today_str = date.today().isoformat()
        record = self._repo.get_by_date(today_str)
        if record is None:
            return None
        return self._to_entry(record)

    def get_by_date(self, target_date: str) -> Optional[ApodEntry]:
        """Return APOD entry for a specific date (YYYY-MM-DD)."""
        record = self._repo.get_by_date(target_date)
        if record is None:
            return None
        return self._to_entry(record)

    def get_recent(self, limit: int = 10) -> List[ApodEntry]:
        """Return the most recent APOD entries."""
        records = self._repo.get_latest(limit=limit)
        return [self._to_entry(r) for r in records]

    @staticmethod
    def _to_entry(record: NasaApod) -> ApodEntry:
        return ApodEntry(
            apod_date=record.apod_date,
            title=record.title,
            explanation=record.explanation,
            url=record.url,
            hdurl=record.hdurl,
            media_type=record.media_type,
            copyright_text=record.copyright_text,
            thumbnail_url=record.thumbnail_url,
        )
