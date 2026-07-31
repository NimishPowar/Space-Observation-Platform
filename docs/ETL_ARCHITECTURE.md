# ETL Architecture Overview

This document describes the architecture for the ETL pipeline that will collect
external astronomy knowledge and persist it in MySQL.

## Separation of Responsibilities

### Extract
The extract stage is responsible for retrieving data from external astronomy
providers such as NASA APIs, ESA data services, and public open-data endpoints.

### Transform
The transform stage is responsible for cleaning, validating, normalizing, and
standardizing raw records before they are published into persistent storage.

### Load
The load stage is responsible for safely inserting or updating records in MySQL,
using idempotent repository patterns and migration-safe schema evolution.

## Placement in the System

The ETL system is intentionally isolated from the Astronomy Engine.

- `astronomy_engine`: computes real-time astronomical facts dynamically using
  Skyfield.
- `etl`: ingests and stores reusable reference knowledge in MySQL.
- `backend`: decides whether a workflow should use dynamic engine output or
  persisted ETL data.
- `frontend`: consumes the backend output and never interacts directly with
  Skyfield or the database.

## Planned Package Responsibilities

- `etl/extract`: source-specific data acquisition components.
- `etl/transform`: normalization and enrichment logic.
- `etl/load`: repository-backed write adapters.
- `etl/schedulers`: scheduled and manual execution entry points.
- `etl/sources`: provider connectors.
- `etl/models`: pipeline-oriented record contracts and staging data models.
- `etl/utils`: retry, validation, and diagnostics helpers.
- `etl/pipelines`: top-level orchestration for ETL execution.
