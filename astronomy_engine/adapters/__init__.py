"""Astronomy engine adapters.

This package contains adapters for ephemeris sources, skyfield data, and
other astronomy-specific external services.
"""

from .skyfield_adapter import SkyfieldAdapter

__all__ = [
    "SkyfieldAdapter",
]
