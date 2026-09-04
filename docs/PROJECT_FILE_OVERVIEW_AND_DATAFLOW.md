# Space Observation Platform: Complete File Overview & Data Flow Documentation

This document provides a comprehensive analysis of every file in the **Space Observation Intelligence Platform** codebase. It outlines what is contained within each file, its architectural responsibility, and how data moves across all system layers—from frontend UI widgets down to lower-level ephemeris adapters, database persistence, and external APIs.

---

## 1. Executive Summary & Architecture Overview

The **Space Observation Platform** is a domain-driven Python and web application designed to compute, visualize, plan, and analyze astronomical observations.

```
       ┌───────────────────────────────────────────────────────────┐
       │             Frontend Layer (Streamlit & Web)              │
       │   app.py | pages/(explore, planner, discovery, learn)     │
       │   moonphase/ & solarsystem/ (3D WebGL Canvas Engines)     │
       └───────────────┬───────────────────────────┬───────────────┘
                       │ HTTP / REST               │ Inline Web View
                       ▼                           ▼
       ┌───────────────────────────────────────────────────────────┐
       │                  Backend API Layer (FastAPI)              │
       │   backend/api/ (main.py, routes.py, dependencies.py)      │
       └───────────────┬───────────────────────────┬───────────────┘
                       │ Use Case Orchestration    │ Use Case Orchestration
                       ▼                           ▼
 ┌───────────────────────────────────┐   ┌───────────────────────────────────┐
 │    Astronomy Calculation Engine    │   │  Persistence & Integration Layer   │
 │   astronomy_engine/ (core,        │   │   database/ (models, repository)  │
 │   services, calculations, adapters│   │   backend/adapters/ (nasa_adapter)│
 └─────────────────┬─────────────────┘   └─────────────────┬─────────────────┘
                   │ Precision Vectors                     │ SQL / HTTP
                   ▼                                       ▼
 ┌───────────────────────────────────┐   ┌───────────────────────────────────┐
 │ JPL Ephemeris Kernel (de421.bsp)  │   │  MySQL DB / NASA APOD REST API    │
 └───────────────────────────────────┘   └───────────────────────────────────┘
```

---

## 2. Comprehensive File-by-File Catalog

### 2.1 Root Configuration & Meta Files

* **[.env.example](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/.env.example)**
  Defines placeholder environment variables for database connections (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`), logging (`LOG_LEVEL`), data directories, and API keys (`NASA_API_KEY`).
* **[.gitignore](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/.gitignore)**
  Specifies git exclusion rules for Python caches (`__pycache__`, `.pytest_cache`), local `.env` files, virtual environments, IDE files, and temporary artifacts.
* **[.streamlit/config.toml](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/.streamlit/config.toml)**
  Streamlit configuration file setting the dark visual theme, primary background/text colors, server port, and browser options.
* **[logging_config.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/logging_config.py)**
  Configures structured Python logging using `logging.config.dictConfig`. Standardizes log formats and log levels across API services, background processes, and calculation modules.
* **[pyproject.toml](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/pyproject.toml)**
  Project build system specification (PEP 518/517). Defines project metadata, dependencies (FastAPI, Streamlit, SQLAlchemy, Skyfield, PyMySQL, Pydantic, HTTPX, pytest), and tool configurations for pytest.
* **[requirements.txt](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/requirements.txt)**
  Pinned Python dependencies file for quick installation via `pip install -r requirements.txt`.
* **[de421.bsp](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/de421.bsp)**
  Binary NASA/JPL DE421 Ephemeris file containing highly accurate planetary position matrices (covering 1900 to 2050) used by Skyfield adapters for precision calculations.
* **Project Specifications & Documentation Markdown Files**:
  * **[API_SPECIFICATION.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/API_SPECIFICATION.md)**: OpenApi request/response specs for REST endpoints (`/moon`, `/planets`, `/events`, `/skymap`, `/planner`, etc.).
  * **[ARCHITECTURE.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/ARCHITECTURE.md)**: Architectural blueprint detailing component boundaries and layer separation.
  * **[CHANGELOG.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/CHANGELOG.md)**: Version history log tracking platform releases and milestone additions.
  * **[DATABASE_DESIGN.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/DATABASE_DESIGN.md)**: Normalized relational schema diagrams and index configurations for MySQL.
  * **[DECISIONS.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/DECISIONS.md)**: Architecture Decision Records (ADRs) explaining choices like Streamlit + FastAPI + Skyfield.
  * **[PROJECT_CONTEXT.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/PROJECT_CONTEXT.md)**: High-level overview of project scope, astronomical objectives, and constraints.
  * **[PROJECT_RULES.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/PROJECT_RULES.md)**: Coding standards, typing rules, and architectural guidelines for contributors.
  * **[PROJECT_VISION.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/PROJECT_VISION.md)**: Product roadmap and future functional aspirations.
  * **[README.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/README.md)**: Developer quick-start guide, installation commands, and system overview.
  * **[REQUIREMENTS.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/REQUIREMENTS.md)**: Functional and non-functional requirement requirements matrix.
  * **[TASKS.md](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/TASKS.md)**: Development task tracking board and operational status.

---

### 2.2 System Configuration (`config/`)

* **[config/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/config/__init__.py)**
  Package marker for the settings module.
* **[config/settings.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/config/settings.py)**
  Centralized settings dataclass (`Settings`) using `python-dotenv`. Reads environment variables (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DATABASE_URL`, `DATA_DIR`, `LOG_LEVEL`) and exposes a singleton `settings` instance.

---

### 2.3 Database & Migrations (`database/` & `alembic/`)

* **[alembic.ini](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/alembic.ini)**
  Alembic database migration configuration file linking migration scripts with SQLAlchemy models.
* **[alembic/env.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/alembic/env.py)**
  Alembic migration runtime script. Sets up migration execution context, imports `database.base.Base`, binds database engines, and runs online/offline schema migrations.
* **[alembic/versions/20260731_001_initial_schema.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/alembic/versions/20260731_001_initial_schema.py)**
  Initial migration revision script. Creates database tables: `users`, `planets`, `celestial_events`, `educational_categories`, `educational_content`, `observation_logs`, `api_cache`, `application_settings`, and `nasa_apod`.
* **[database/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/__init__.py)**
  Package marker exporting database connection sessions and models.
* **[database/base.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/base.py)**
  Defines the base SQLAlchemy ORM class `Base(DeclarativeBase)` used by all database entities.
* **[database/connection.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/connection.py)**
  Creates and manages the SQLAlchemy `Engine` instance using `settings.database_url`. Includes connection pooling parameters and connection testing utilities.
* **[database/models.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/models.py)**
  Contains full SQLAlchemy ORM mappings for platform entities:
  - `User`: User profile records.
  - `Planet`: Static planetary characteristics (mass, radius, semi-major axis, orbital period).
  - `CelestialEvent`: Astronomical events (conjunctions, meteor showers, eclipses).
  - `EducationalCategory`: Categories for educational articles (`solar-system`, `deep-sky`, `observing-guides`).
  - `EducationalContent`: Informational articles with titles, slugs, bodies, and excerpts.
  - `ObservationLog`: Log records of observations recorded by users.
  - `ApiCache`: JSON payload cache table storing external API responses with expiration tracking.
  - `ApplicationSetting`: System key-value preferences.
  - `NasaApod`: Stored APOD records (title, date, explanation, media URLs, copyright).
* **[database/repository.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/repository.py)**
  Implements the Repository Pattern (`DatabaseRepository`). Wraps SQLAlchemy session queries to perform CRUD operations for planets, celestial events, educational content, observation logs, APOD records, and API cache entities.
* **[database/seeds.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/seeds.py)**
  Database seeding utility that populates initial reference data for planets, educational categories/content, and baseline celestial events upon initial setup.
* **[database/session.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/database/session.py)**
  Configures the SQLAlchemy `sessionmaker` factory and provides `get_db()` context manager and dependency provider for DB session lifecycles.

---

### 2.4 Astronomy Calculation Engine (`astronomy_engine/`)

* **[astronomy_engine/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/__init__.py)**
  Exposes the top-level `AstronomyEngine` interface and public domain data structures.
* **`astronomy_engine/core/`**:
  * **[domain.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/core/domain.py)**: Domain dataclasses representing astronomical concepts: `Location`, `ObservationContext`, `Position` (Altitude/Azimuth/RA/Dec), `MoonSummary`, `PlanetPosition`, `SolarSummary`, `VisibilityWindow`, `StarPosition`, `ConstellationData`, `SkyMapData`, and `ObservationScore`.
  * **[engine.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/core/engine.py)**: High-level `AstronomyEngine` facade class. Coordinates moon, planet, sun, star, constellation, and visibility services to answer complex queries.
  * **[factory.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/core/factory.py)**: Factory functions (`create_astronomy_engine()`, `create_stub_engine()`) for instantiating the engine with either real Skyfield adapters or stub adapters.
* **`astronomy_engine/calculations/`**:
  * **[astronomy.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/calculations/astronomy.py)**: Pure mathematical and trigonometrical routines: Julian date conversion, Sidereal time, RA/Dec to Azimuth/Altitude coordinate transformations, lunar illumination phase angle formulas, angular separation, and refraction corrections.
* **`astronomy_engine/adapters/`**:
  * **[ephemeris_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/adapters/ephemeris_adapter.py)**: Abstract base interface for ephemeris computation providers.
  * **[skyfield_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/adapters/skyfield_adapter.py)**: Abstract adapter interface isolating lower-level Skyfield calls from domain services.
* **`astronomy_engine/implementations/`**:
  * **[skyfield_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/implementations/skyfield_adapter.py)**: Concrete Skyfield adapter interfacing with `de421.bsp` ephemeris files. Computes topocentric position vectors, lunar phases, and solar illumination.
  * **[skyfield_runtime_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/implementations/skyfield_runtime_adapter.py)**: Runtime adapter managing Skyfield timescale loading (`ts.now()`, `ts.utc()`) and observer position creation.
  * **[adapter_services.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/implementations/adapter_services.py)**: Adapter-backed domain service implementations binding Skyfield computations to domain interfaces.
  * **[stub_services.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/implementations/stub_services.py)**: Deterministic mock service implementations for offline development and fast testing without external ephemeris files.
* **`astronomy_engine/services/`**:
  * **[moon_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/moon_service.py)**: Computes moon phase, fraction illuminated, sub-lunar coordinates, and rise/set timestamps.
  * **[planet_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/planet_service.py)**: Computes coordinates (RA, Dec, Alt, Az), distance from Earth (AU), and visual magnitude for major planets.
  * **[sun_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/sun_service.py)**: Calculates sunrise, sunset, solar noon, solar altitude/azimuth, and astronomical twilight transitions.
  * **[star_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/star_service.py)**: Computes real-time positions for catalogued bright stars above a specified minimum altitude horizon.
  * **[constellation_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/constellation_service.py)**: Resolves visible constellation patterns, line segments between stars, and boundary mapping.
  * **[visibility_service.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/astronomy_engine/services/visibility_service.py)**: Evaluates visibility conditions (is target above horizon, is sun below twilight limit, moon interference) to generate visibility windows and quality scores.

---

### 2.5 Backend API Layer (`backend/`)

* **[backend/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/__init__.py)**
  Package initialization marker.
* **`backend/api/`**:
  * **[main.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/api/main.py)**: FastAPI application entrypoint. Configures CORS middleware, registers router prefix (`/api/v1`), sets up startup event handlers (DB table verification, seeding), and exposes `/health` endpoint.
  * **[routes.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/api/routes.py)**: Implements all REST endpoints (`/moon`, `/planets`, `/stars`, `/constellations`, `/skymap`, `/visibility`, `/planner`, `/sun`, `/events`, `/discovery/*`, `/learn/*`, `/apod/*`). Handles parameter extraction, calls domain use cases, and serializes responses.
  * **[dependencies.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/api/dependencies.py)**: FastAPI dependency injection handlers (`Depends`). Provides instances of `DatabaseRepository`, `AstronomyEngine`, `AstronomyUseCase`, `EventsUseCase`, `LearnUseCase`, `NasaApodUseCase`, and `ObservationPlannerUseCase`.
* **`backend/adapters/`**:
  * **[astronomy_engine_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/adapters/astronomy_engine_adapter.py)**: Adapter converting raw `AstronomyEngine` output types into API schemas.
  * **[database_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/adapters/database_adapter.py)**: Adapts database repository queries into FastAPI/Pydantic usable dict formats.
  * **[nasa_adapter.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/adapters/nasa_adapter.py)**: HTTP integration client interfacing with official NASA APOD API endpoint (`https://api.nasa.gov/planetary/apod`). Includes network error handling and payload parsing.
* **`backend/use_cases/`**:
  * **[astronomy_use_case.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/use_cases/astronomy_use_case.py)**: Orchestrates requests for planetary positions, lunar info, solar state, stars, constellations, and sky maps via `AstronomyEngine`.
  * **[events_use_case.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/use_cases/events_use_case.py)**: Retrieves and filters upcoming astronomical events from database repository.
  * **[learn_use_case.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/use_cases/learn_use_case.py)**: Fetches educational categories, featured topics, topic details by slug, and object guides from MySQL.
  * **[nasa_apod_use_case.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/use_cases/nasa_apod_use_case.py)**: Orchestrates APOD retrieval logic: checks local database repository for cached APOD record for target date; if missing, invokes `NasaAdapter` to fetch from NASA API and persists to DB cache.
  * **[observation_planner.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/use_cases/observation_planner.py)**: Generates ranked target lists and custom observation schedules for a given location, scoring target altitude, dark sky quality, and lunar clearance.
* **`backend/schemas/`**:
  * **[models.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/schemas/models.py)**: Pydantic schemas for API inputs and responses (`MoonResponse`, `PlanetPositionResponse`, `VisibilityWindowResponse`, `ObservationScoreResponse`, `CelestialEventResponse`, `SolarStateResponse`, `StarResponse`, `ConstellationResponse`, `SkyMapResponse`).
  * **[apod_models.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/backend/schemas/apod_models.py)**: Pydantic data schemas for APOD responses (`ApodResponse`).

---

### 2.6 Frontend User Interface Layer (`frontend/`)

* **[frontend/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/__init__.py)**
  Package marker for frontend module.
* **[frontend/app.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/app.py)**
  Main Streamlit application entry point. Sets page configuration, sidebar navigation menu, common observer location input controls (latitude, longitude, city search), and routes to selected page modules.
* **[frontend/client.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/client.py)**
  `ApiClient` HTTP wrapper class. Communicates with backend REST API endpoints using `requests`. Includes `search_city()` helper using OpenStreetMap Nominatim API for geocoding user city queries into lat/long coordinates.
* **[frontend/ui.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/ui.py)**
  Reusable Streamlit custom styling functions, metric card renders, CSS injections, header formatters, and status badges.
* **`frontend/pages/`**:
  * **[explore.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/pages/explore.py)**: Interactive Exploration view. Renders real-time planetary position tables, altitude/azimuth sky charts, and embeds the interactive 3D Solar System WebGL Canvas visualizer.
  * **[planner.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/pages/planner.py)**: Observation Planner UI view. Allows selection of target celestial bodies, calculates target visibility windows, generates ranked observation score charts, and lists solar twilight bounds.
  * **[discovery.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/pages/discovery.py)**: Discovery & APOD view. Features NASA Astronomy Picture of the Day media viewer, historical APOD gallery, interactive lunar phase simulator, and embedded 3D Moon visualizer.
  * **[learn.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/frontend/pages/learn.py)**: Educational Knowledge Hub. Renders searchable astronomy articles, categories (Solar System, Deep Sky, Observational Astronomy), and celestial object reference guides.

---

### 2.7 Data Ingestion Pipelines (`etl/`)

* **[etl/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/__init__.py)**
  Package marker for ETL processes.
* **[etl/pipelines/base.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/pipelines/base.py)**
  Abstract base pipeline class defining standard ETL execution lifecycle (`extract()`, `transform()`, `load()`, `run()`).
* **[etl/pipelines/nasa_apod_pipeline.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/pipelines/nasa_apod_pipeline.py)**
  Concrete ETL pipeline fetching batch APOD entries from external NASA API, converting raw payloads into `NasaApod` database models, and saving records to MySQL.
* **[etl/extract/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/extract/)**, **[etl/transform/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/transform/)**, **[etl/load/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/load/)**, **[etl/models/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/models/)**, **[etl/schedulers/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/schedulers/)**, **[etl/sources/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/sources/)**, **[etl/utils/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/etl/utils/)**: Subpackages structured for modular data source connectors, transformation transformers, and cron scheduling extensions.

---

### 2.8 Analytics Dashboard (`analytics/`)

* **[analytics/__init__.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/analytics/__init__.py)**
  Package marker.
* **[analytics/dashboard.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/analytics/dashboard.py)**
  Standalone analytics dashboard built with Streamlit. Connects to database repository to calculate observation statistics, query execution metrics, target popularity counts, and logs summary charts.

---

### 2.9 Web-Based 3D Visualizers (`moonphase/` & `solarsystem/`)

* **`moonphase/`**: Standalone HTML5 / Three.js / Canvas 3D interactive lunar visualizer.
  * **[moonphase/index.html](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/moonphase/index.html)**: HTML container structure loading Three.js and custom scripts.
  * **[moonphase/script.js](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/moonphase/script.js)**: WebGL rendering logic. Renders textured 3D sphere for Moon, directionally lit by Sun position to simulate lunar illumination phases dynamically based on slider/date inputs.
  * **[moonphase/style.css](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/moonphase/style.css)**: Modern dark UI styles for full-screen web canvas and controls.
  * **[moonphase/images/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/moonphase/images/)**: Texture maps (`moon.jpg`, `earth_daymap.jpg`, `earth_nightmap.jpg`, `sun.jpg`).
* **`solarsystem/`**: Standalone HTML5 / Three.js 3D Solar System visualizer.
  * **[solarsystem/index.html](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/solarsystem/index.html)**: Main HTML host page.
  * **[solarsystem/script.js](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/solarsystem/script.js)**: 3D scene engine. Loads planetary spheres, orbit tracks, Saturn rings, lighting, and camera rotation controls.
  * **[solarsystem/style.css](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/solarsystem/style.css)**: UI styling for celestial body selector panel and information overlays.
  * **[solarsystem/images/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/solarsystem/images/)**: Planetary textures and ring transparency maps for Sun, Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.

---

### 2.10 Automated Test Suite (`tests/`)

* **[tests/test_project_structure.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/test_project_structure.py)**: Verifies presence of key application files, directories, and package exports.
* **[tests/test_astronomy_engine_contract.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/test_astronomy_engine_contract.py)**: Contract tests checking `AstronomyEngine` calculations, domain model returns, and adapter integration.
* **[tests/test_nasa_apod.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/test_nasa_apod.py)**: Unit and mock tests for NASA APOD API fetching and caching logic.
* **[tests/test_skymap_stars_constellations.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/test_skymap_stars_constellations.py)**: Validates catalog star positions, altitude filtering, constellation rendering data, and sky map coordinate conversion.
* **[tests/backend/](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/backend/)**:
  * `test_events_api.py` & `test_events_use_case.py`: FastAPI endpoint & use case tests for event endpoints.
  * `test_learn_api.py` & `test_learn_use_case.py`: Tests for educational content endpoints.
  * `test_observation_planner.py`: Tests observation scoring and visibility window algorithms.
* **[tests/database/test_repository_layer.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/database/test_repository_layer.py)**: Tests database repository methods against in-memory/mock sessions.
* **[tests/frontend/test_frontend_api_client.py](file:///c:/Users/NIMISH/Desktop/Space%20Observation%20Platform/tests/frontend/test_frontend_api_client.py)**: Tests Streamlit `ApiClient` REST communication and error handling.

---

## 3. End-to-End Data Flow Architecture

### 3.1 Flow 1: Observation Planner Target Scoring & Visibility Calculation

This workflow executes when a user opens the **Planner** page in Streamlit to generate an optimal observation schedule.

```
 [User Input: Lat/Long/Time]
            │
            ▼
 [frontend/pages/planner.py] ──(requests.get)──► [backend/api/routes.py: /api/v1/planner]
                                                               │
                                                               ▼
                                             [backend/api/dependencies.py]
                                                               │
                                                               ▼
                                         [backend/use_cases/observation_planner.py]
                                                               │
                                                               ▼
                                              [astronomy_engine/core/engine.py]
                                                               │
                                   ┌───────────────────────────┴───────────────────────────┐
                                   ▼                                                       ▼
                [astronomy_engine/services/planet_service]           [astronomy_engine/services/sun_service]
                                   │                                                       │
                                   └───────────────────────────┬───────────────────────────┘
                                                               │
                                                               ▼
                                        [astronomy_engine/implementations/skyfield_adapter]
                                                               │
                                                               ▼
                                                 [JPL Ephemeris File: de421.bsp]
```

**Step-by-Step Flow Description**:
1. **User Interaction**: User inputs observer location (e.g. Lat: `12.97`, Long: `77.59`), observation timestamp, and desired target list on `frontend/pages/planner.py`.
2. **Frontend Request**: `planner.py` invokes `ApiClient.get_planner()` in `frontend/client.py`, sending an HTTP GET request to `/api/v1/planner` with query parameters.
3. **API Routing**: FastAPI `backend/api/routes.py` receives request, parses timestamps into timezone-aware `datetime`, builds an `ObservationContext` dataclass, and resolves dependencies via `backend/api/dependencies.py`.
4. **Use Case Execution**: `ObservationPlannerUseCase` in `backend/use_cases/observation_planner.py` executes `estimate_window()`.
5. **Engine Calculations**:
   - Calls `AstronomyEngine.get_planetary_positions()` to calculate topocentric RA, Dec, Altitude, Azimuth, and visual magnitude via `PlanetService` and `SkyfieldAdapter`.
   - Calls `AstronomyEngine.get_solar_summary()` via `SunService` to verify twilight state (Sun altitude < -12° or -18°).
   - Calls `MoonService` to check lunar phase and distance to avoid lunar glare interference.
6. **Ephemeris Resolution**: `SkyfieldAdapter` computes vector positions using the binary JPL ephemeris kernel (`de421.bsp`).
7. **Scoring Algorithm**: `ObservationPlannerUseCase` computes a quality score (0 - 100) based on altitude above horizon, darkness of sky, and lunar separation.
8. **Response Serialization**: Route handler serializes domain dataclasses to Pydantic JSON responses (`ObservationScoreResponse`) and returns HTTP 200 OK.
9. **UI Visualization**: `frontend/pages/planner.py` receives JSON, passes metrics to `frontend/ui.py`, and renders interactive visibility charts and observation tables.

---

### 3.2 Flow 2: NASA Astronomy Picture of the Day (APOD) Fetching & DB Caching

This workflow handles fetching space media while minimizing external network requests through database caching.

```
 [User opens Discovery Page]
            │
            ▼
 [frontend/pages/discovery.py] ──► [backend/api/routes.py: /api/v1/apod/today]
                                                       │
                                                       ▼
                                     [backend/use_cases/nasa_apod_use_case.py]
                                                       │
                                                       ▼
                                     [database/repository.py: get_apod_by_date]
                                                       │
                           ┌───────────────────────────┴───────────────────────────┐
                      (If Cached)                                             (If Miss)
                           │                                                       │
                           ▼                                                       ▼
                 [Return MySQL Record]                                 [backend/adapters/nasa_adapter.py]
                                                                                   │
                                                                                   ▼
                                                                        [HTTP GET api.nasa.gov]
                                                                                   │
                                                                                   ▼
                                                                       [database/repository.py: create_apod]
                                                                                   │
                                                                                   ▼
                                                                          [Save to MySQL DB]
```

**Step-by-Step Flow Description**:
1. **Frontend Trigger**: User navigates to the **Discovery** tab in Streamlit (`frontend/pages/discovery.py`).
2. **Frontend Client**: `ApiClient.get_apod_today()` sends request to `/api/v1/apod/today`.
3. **Use Case Orchestration**: `NasaApodUseCase` in `backend/use_cases/nasa_apod_use_case.py` receives call.
4. **Cache Check**: `NasaApodUseCase` calls `DatabaseRepository.get_apod_by_date(today_str)` to query local MySQL table `nasa_apod`.
5. **Cache Hit Path**: If APOD record exists in DB, it is immediately returned to backend router without calling NASA API.
6. **Cache Miss Path**:
   - If not found in DB, `NasaApodUseCase` calls `NasaAdapter.fetch_apod(today_str)`.
   - `NasaAdapter` sends HTTPS GET request to `https://api.nasa.gov/planetary/apod` using configured `NASA_API_KEY`.
   - Received raw JSON is parsed into Pydantic schema `ApodResponse`.
   - `NasaApodUseCase` calls `DatabaseRepository.create_apod(...)` to insert record into MySQL `nasa_apod` table for future requests.
7. **Response to Client**: JSON representation returned to Streamlit UI and displayed with high-resolution image viewer, title, date, and text explanation.

---

### 3.3 Flow 3: Interactive 3D WebGL Visualizers (Moon Phase & Solar System)

This workflow demonstrates how standalone web components render 3D visualizers directly within the application UI.

```
 [Streamlit Frontend Component]
            │
            ▼
 [components.iframe() / html()]
            │
            ▼
 [moonphase/index.html OR solarsystem/index.html]
            │
            ▼
 [script.js (Three.js WebGL Renderer)] ◄──► [Local Image Textures (images/*.jpg)]
            │
            ▼
 [Interactive 3D Canvas in Browser DOM]
```

**Step-by-Step Flow Description**:
1. **Component Mount**: `frontend/pages/discovery.py` or `frontend/pages/explore.py` calls Streamlit `st.components.v1.iframe` or reads `index.html`.
2. **HTML Page Load**: Browser loads HTML container (`moonphase/index.html` or `solarsystem/index.html`).
3. **Script Execution**: `script.js` initializes Three.js WebGL Renderer, Scene, Camera, and OrbitControls.
4. **Texture Asset Loading**: WebGL texture loader asynchronously loads sphere diffuse texture maps (`earth_daymap.jpg`, `moon.jpg`, `saturn.jpg`) from local assets directory.
5. **Render Loop**: `requestAnimationFrame` loop updates rotation matrices, planet orbital positions, and directional light vector representing sunlight.
6. **User Interaction**: Dragging mouse updates camera view matrices in real time inside WebGL canvas.

---

## 4. Summary Matrix of File Dependencies

| Layer | Primary Modules | Key Dependencies | Target Consumers |
| :--- | :--- | :--- | :--- |
| **Config** | `config/settings.py` | `python-dotenv`, `os`, `pathlib` | Entire platform |
| **Database** | `database/models.py`, `repository.py` | `sqlalchemy`, `pymysql` | Backend Use Cases, ETL, Analytics |
| **Astronomy Engine** | `astronomy_engine/core/engine.py` | `skyfield`, `numpy`, `de421.bsp` | Backend Use Cases |
| **Backend API** | `backend/api/routes.py` | `fastapi`, `pydantic` | Frontend `ApiClient` |
| **Frontend UI** | `frontend/app.py`, `pages/*.py` | `streamlit`, `httpx`, `requests` | End-user Web Browser |
| **3D Visualizers** | `moonphase/*`, `solarsystem/*` | `Three.js`, `HTML5 Canvas` | Streamlit Iframes / Standalone HTML |
| **ETL Pipelines** | `etl/pipelines/nasa_apod_pipeline.py` | `requests`, `sqlalchemy` | MySQL Database |

---
*Document compiled and verified against project repository commit tree.*
