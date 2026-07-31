# Architecture Overview

This document describes the platform architecture after the MySQL-first and
ETL-first design update.

## Architectural Direction

The platform now follows a layered, clean-architecture model with a strict
separation of concerns:

- `frontend`: user-facing UI and experience composition.
- `backend`: API boundary, use cases, and dependency injection.
- `astronomy_engine`: real-time astronomical calculations using Skyfield through
  isolated adapters.
- `database`: SQLAlchemy repository abstractions and persistence coordination.
- `etl`: external knowledge ingestion pipeline divided into extraction,
  transformation, loading, scheduling, and source-specific packaging.
- `analytics`: analytics pipelines and reporting composition.
- `datasets`: curated data and dataset preparation assets.
- `config`: environment-driven settings, including MySQL and Alembic defaults.
- `docs`: documentation and architecture references.
- `tests`: validation and contract smoke tests.

## Persistence Strategy

The relational persistence layer uses MySQL as the primary storage engine.
SQLAlchemy ORM provides the repository boundary, and Alembic handles future
schema migrations. Database access is kept separate from business logic and
from the astronomy engine.

## ETL Separation

The ETL pipeline has a dedicated package boundary and a clear stage separation:

- `etl/extract`: data acquisition from NASA, ESA, and public astronomy datasets.
- `etl/transform`: normalization, validation, deduplication, and enrichment.
- `etl/load`: safe database writes through idempotent repository behavior.
- `etl/schedulers`: scheduled/manual orchestration hooks.
- `etl/sources`: source adapters for external providers.
- `etl/models`: staging and pipeline-related domain records.
- `etl/utils`: common logging, retries, and validation helpers.
- `etl/pipelines`: top-level orchestration entry points.

## Design Principle

Skyfield remains responsible only for dynamic, real-time astronomy calculations.
The ETL components are responsible for collecting reusable external astronomy
knowledge and storing it in MySQL. The backend decides which source of truth to
use for a given workflow.
