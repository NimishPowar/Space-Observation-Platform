"""Centralized logging configuration for the project."""

from __future__ import annotations

import logging
from logging import Logger
from typing import Optional

from config.settings import settings


def configure_logging(level: Optional[str] = None) -> Logger:
    """Configure the root application logger."""
    log_level = level or settings.log_level
    logger = logging.getLogger("space_observation_platform")
    logger.setLevel(log_level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
