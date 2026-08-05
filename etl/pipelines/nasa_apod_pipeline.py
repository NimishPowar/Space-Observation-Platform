"""NASA APOD ETL pipeline: Extract from NASA API -> Transform -> Load to MySQL."""

from __future__ import annotations

import logging
from datetime import date, timedelta
from typing import Any, List, Optional

from backend.adapters.nasa_adapter import ApodResult, NasaAdapter
from database.models import NasaApod
from database.repository import NasaApodRepository
from database.session import DatabaseSessionManager
from etl.pipelines.base import (
    BaseETLPipeline,
    ComposableETLPipeline,
    Extractor,
    Loader,
    PipelineResult,
    Transformer,
)

logger = logging.getLogger(__name__)


class ApodExtractor(Extractor[ApodResult]):
    """Extracts APOD data from NASA API."""

    def __init__(self, nasa_adapter: Optional[NasaAdapter] = None) -> None:
        self._adapter = nasa_adapter or NasaAdapter()

    def extract(self, **kwargs: Any) -> List[ApodResult]:
        """Extract APOD entries. kwargs can include 'start_date' and 'end_date' or 'target_date'."""
        target_date = kwargs.get("target_date")
        start_date = kwargs.get("start_date")
        end_date = kwargs.get("end_date")

        if start_date:
            return self._adapter.get_apod_range(
                start_date=start_date,
                end_date=end_date,
            )
        else:
            result = self._adapter.get_apod(target_date=target_date)
            return [result]


class ApodTransformer(Transformer[ApodResult, NasaApod]):
    """Transforms NASA APOD API results into ORM model instances."""

    def transform(self, raw_records: List[ApodResult]) -> List[NasaApod]:
        transformed: List[NasaApod] = []
        for record in raw_records:
            if not record.apod_date or not record.title:
                logger.warning("Skipping APOD record with missing date or title")
                continue
            apod = NasaApod(
                apod_date=record.apod_date,
                title=record.title,
                explanation=record.explanation,
                url=record.url,
                hdurl=record.hdurl,
                media_type=record.media_type,
                copyright_text=record.copyright_text,
                thumbnail_url=record.thumbnail_url,
                source_api="nasa_apod",
            )
            transformed.append(apod)
        return transformed


class ApodLoader(Loader[NasaApod]):
    """Loads APOD entries into database via repository."""

    def __init__(self, session_manager: Optional[DatabaseSessionManager] = None) -> None:
        self._session_manager = session_manager or DatabaseSessionManager()

    def load(self, records: List[NasaApod]) -> int:
        session = self._session_manager.get_session()
        try:
            repo = NasaApodRepository(session)
            count = 0
            for record in records:
                repo.upsert(record)
                count += 1
            session.commit()
            return count
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class NasaApodPipeline(BaseETLPipeline):
    """Complete NASA APOD ETL Pipeline.

    Extracts APOD data from NASA, transforms to internal model,
    and loads/upserts into database.
    """

    def __init__(
        self,
        nasa_adapter: Optional[NasaAdapter] = None,
        session_manager: Optional[DatabaseSessionManager] = None,
    ) -> None:
        self._pipeline = ComposableETLPipeline(
            extractor=ApodExtractor(nasa_adapter=nasa_adapter),
            transformer=ApodTransformer(),
            loader=ApodLoader(session_manager=session_manager),
            pipeline_name="nasa_apod",
        )

    @property
    def name(self) -> str:
        return "nasa_apod"

    def run(self, **kwargs: Any) -> PipelineResult:
        """Run the NASA APOD ETL pipeline."""
        return self._pipeline.run(**kwargs)

    def run_today(self) -> PipelineResult:
        """Convenience method to fetch today's APOD."""
        return self.run(target_date=date.today())

    def run_last_n_days(self, days: int = 7) -> PipelineResult:
        """Convenience method to fetch the last N days of APOD entries."""
        end = date.today()
        start = end - timedelta(days=days - 1)
        return self.run(start_date=start, end_date=end)
