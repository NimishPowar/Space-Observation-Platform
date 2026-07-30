"""Abstract Visibility service interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from astronomy_engine.core.domain import ObservationContext, VisibilityWindow


class VisibilityService(ABC):
    """Public visibility service interface for observation planning."""

    @abstractmethod
    def compute_visibility(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        """Compute visibility windows for the requested set of objects."""
        raise NotImplementedError

    @abstractmethod
    def compute_best_observation_windows(
        self,
        context: ObservationContext,
        object_names: Optional[List[str]] = None,
    ) -> List[VisibilityWindow]:
        """Compute prioritized observation windows for the requested context."""
        raise NotImplementedError

    @abstractmethod
    def is_object_visible(
        self,
        object_name: str,
        context: ObservationContext,
    ) -> bool:
        """Return whether the requested object is visible in the given context."""
        raise NotImplementedError
