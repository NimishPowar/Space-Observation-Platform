# Changelog

## Version 0.1.0

Project initialized.
- Clean Architecture repository structure created
- Environment configuration and initial documentation completed

---

## Version 0.2.0

Astronomy Engine Core
- Implemented `AstronomyEngine` domain models (`MoonPhase`, `PlanetPosition`, `SolarState`, `VisibilityWindow`, `Star`, `Constellation`)
- Integrated `SkyfieldRuntimeAdapter` with `de421.bsp` ephemeris files
- Built `MoonService`, `PlanetService`, `SunService`, `VisibilityService`, `StarService`, and `ConstellationService` abstractions

---

## Version 0.3.0

Explore Module
- Implemented real-time night sky map rendering with stars and constellation connectivity
- Added visible planet positions, lunar state, and twilight boundary calculations
- Built Streamlit Explore dashboard UI (`frontend/pages/explore.py`)

---

## Version 0.4.0

Observation Planner Module
- Built target object visibility scoring engine
- Implemented observation window calculation algorithms
- Created celestial event repository and API endpoint (`/api/events`)

---

## Version 0.5.0

Learn Module Initial Integration
- Wired `/api/learn/{object_name}` to MySQL via `LearnUseCase` and `EducationalContentRepository`
- Wired `/api/events` to MySQL via `EventsUseCase` and `CelestialEventRepository`
- Added repository lookup helpers and backend/API test suite

---

## Version 0.6.0

NASA APOD Integration & ETL Pipeline
- Created `NasaApod` SQLAlchemy ORM model and `NasaApodRepository`
- Built `NasaAdapter` to interface with NASA public APOD API
- Implemented `NasaApodPipeline` following `Extractor` → `Transformer` → `Loader` ETL framework
- Added `/api/apod/today`, `/api/apod/recent`, and `/api/apod/{target_date}` FastAPI routes

---

## Version 0.7.0

Discovery Hub & 3D Interactive Simulators
- Expanded Learn page into **Discovery** hub with 3 dedicated tabs
- Module 1: **Astronomy Basics** with 8 seeded MySQL topics, category filtering, and live keyword search
- Module 2: **3D Solar System View** with interactive 3D WebGL orbit viewer, speed presets, and simulated clock
- Module 3: **3D Moon Phase Simulator** with 3D directional lighting model paired with calculated illumination, lunar age, phase angle, and rise/set timing via `/api/discovery/moon-phase`

---

## Version 0.8.0

Architecture Refinements & Auto-Healing Pipelines
- Wired `use_stubs` flag in `create_astronomy_engine` factory to enable stub test doubles (`StubMoonService`, `StubPlanetService`, `StubSunService`, `StubVisibilityService`)
- Added auto-triggering ETL execution in `NasaApodUseCase` to fetch missing APOD entries automatically
- Created dynamic `seed_celestial_events` to populate upcoming event schedules
- Cleaned Streamlit sidebar navigation and synchronized `.streamlit/config.toml`
- Updated project documentation (`README.md`, `ARCHITECTURE.md`, `DATABASE_DESIGN.md`, `API_SPECIFICATION.md`, `TASKS.md`) to reflect exact source code state