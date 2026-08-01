"""Streamlit page package for the frontend UI.

This package contains the minimal page modules used by the application
navigation shell.
"""

from frontend.pages.events import render as render_events
from frontend.pages.explore import render as render_explore
from frontend.pages.learn import render as render_learn
from frontend.pages.planner import render as render_planner

__all__ = [
    "render_events",
    "render_explore",
    "render_learn",
    "render_planner",
]
