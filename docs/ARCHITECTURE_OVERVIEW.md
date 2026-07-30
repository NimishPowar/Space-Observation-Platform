# Architecture Overview

This document describes the initial folder structure for the Space Observation
Intelligence Platform and explains the purpose of each major package.

## Architecture

The platform follows clean architecture principles by separating the system into
independent layers:

- `frontend`: User-facing UI components and page composition.
- `backend`: API boundary, use cases, adapters, and schema definitions.
- `astronomy_engine`: Core domain logic for astronomical calculations.
- `database`: Database connectivity and repository abstractions.
- `analytics`: Analytics and dashboard composition modules.
- `datasets`: Dataset loading and preparation utilities.
- `config`: Environment-driven settings and application configuration.
- `docs`: Supporting documentation and architecture reference.
- `tests`: Automated tests to validate modules and structure.

Each package is initialized as a Python package using `__init__.py`.

## Folder Purpose

- `backend/`: Hosts backend application code organized by clean architecture
  boundaries. It isolates API and use-case logic from infrastructure adapters.

- `frontend/`: Contains Streamlit frontend entrypoints and page modules.

- `astronomy_engine/`: Contains astronomy domain modules, calculation placeholders,
  and adapters for ephemeris-related data.

- `database/`: Contains database connection and repository abstraction modules.

- `analytics/`: Contains analytics dashboard placeholders and visualization
  orchestration components.

- `datasets/`: Contains dataset loader placeholders to manage curated data assets.

- `tests/`: Contains placeholder tests and package initialization for future test
  development.

- `docs/`: Contains documentation artifacts that describe architecture and project
  decisions.

- `config/`: Centralized application settings and environment-aware configuration.

- `logging_config.py`: Centralized logging setup for consistent application
  diagnostics.
