"""Base pipeline contracts for ETL orchestration.

This module is intentionally kept as a placeholder so later phases can add
concrete ETL pipeline implementations without changing the public package
structure.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseETLPipeline(ABC):
    """Abstract pipeline contract for ETL execution."""

    @abstractmethod
    def run(self) -> None:
        """Run the pipeline."""
