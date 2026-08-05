"""Pydantic response models for APOD and enhanced planner endpoints."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class ApodResponse(BaseModel):
    apod_date: str
    title: str
    explanation: Optional[str] = None
    url: Optional[str] = None
    hdurl: Optional[str] = None
    media_type: Optional[str] = None
    copyright_text: Optional[str] = None
    thumbnail_url: Optional[str] = None
