"""Base pipeline contracts for ETL orchestration.

Provides abstract base classes for Extract, Transform, Load, and Pipeline
components. Each concrete pipeline implements these contracts.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, List, Optional, TypeVar

logger = logging.getLogger(__name__)

RawT = TypeVar("RawT")
TransformedT = TypeVar("TransformedT")


@dataclass
class PipelineResult:
    """Summary of a pipeline execution."""

    pipeline_name: str
    status: str  # 'success', 'partial', 'failed'
    records_extracted: int = 0
    records_transformed: int = 0
    records_loaded: int = 0
    errors: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None


class Extractor(ABC, Generic[RawT]):
    """Abstract extractor that pulls data from an external source."""

    @abstractmethod
    def extract(self, **kwargs: Any) -> List[RawT]:
        """Extract raw records from the source."""


class Transformer(ABC, Generic[RawT, TransformedT]):
    """Abstract transformer that converts raw data into internal models."""

    @abstractmethod
    def transform(self, raw_records: List[RawT]) -> List[TransformedT]:
        """Transform raw records into internal model objects."""


class Loader(ABC, Generic[TransformedT]):
    """Abstract loader that persists transformed data."""

    @abstractmethod
    def load(self, records: List[TransformedT]) -> int:
        """Load transformed records into persistent storage. Returns count loaded."""


class BaseETLPipeline(ABC):
    """Abstract pipeline contract for ETL execution."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable pipeline name."""

    @abstractmethod
    def run(self, **kwargs: Any) -> PipelineResult:
        """Run the full Extract -> Transform -> Load pipeline."""


class ComposableETLPipeline(BaseETLPipeline):
    """Pipeline that composes an Extractor, Transformer, and Loader."""

    def __init__(
        self,
        extractor: Extractor,
        transformer: Transformer,
        loader: Loader,
        pipeline_name: str = "generic",
    ) -> None:
        self._extractor = extractor
        self._transformer = transformer
        self._loader = loader
        self._pipeline_name = pipeline_name

    @property
    def name(self) -> str:
        return self._pipeline_name

    def run(self, **kwargs: Any) -> PipelineResult:
        result = PipelineResult(
            pipeline_name=self.name,
            status="failed",
            started_at=datetime.now(timezone.utc),
        )
        try:
            raw = self._extractor.extract(**kwargs)
            result.records_extracted = len(raw)
            logger.info("%s: extracted %d records", self.name, len(raw))

            transformed = self._transformer.transform(raw)
            result.records_transformed = len(transformed)
            logger.info("%s: transformed %d records", self.name, len(transformed))

            loaded_count = self._loader.load(transformed)
            result.records_loaded = loaded_count
            logger.info("%s: loaded %d records", self.name, loaded_count)

            result.status = "success"
        except Exception as exc:
            logger.error("%s: pipeline failed: %s", self.name, exc)
            result.errors.append(str(exc))
            result.status = "failed"
        finally:
            result.completed_at = datetime.now(timezone.utc)
        return result
