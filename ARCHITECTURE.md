# System Architecture

The **Space Observation Intelligence Platform** follows Clean Architecture principles, isolating core domain calculation logic, application use cases, data persistence repositories, and presentation layers.

---

## 🏛️ Layered Architecture Diagram

```
                              ┌────────────────────────┐
                              │   Streamlit Frontend   │
                              │    (frontend/pages)    │
                              └───────────┬────────────┘
                                          │ HTTP / Client API
                                          ▼
                              ┌────────────────────────┐
                              │  FastAPI Backend API   │
                              │   (backend/api/routes) │
                              └───────────┬────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
     ┌────────────────────────┐                      ┌────────────────────────┐
     │   Backend Use Cases    │                      │   ETL Pipeline Layer   │
     │  (backend/use_cases)   │                      │ (etl/pipelines/apod)   │
     └───────┬────────┬───────┘                      └───────────┬────────────┘
             │        │                                          │
             │        └───────────────────┐                      │
             ▼                            ▼                      ▼
┌────────────────────────┐    ┌──────────────────────┐┌──────────────────────┐
│    Astronomy Engine    │    │ Repository Layer     ││ NASA Adapter         │
│ (astronomy_engine/core)│    │ (database/repository)││(backend/adapters/nasa│
└────────────┬───────────┘    └──────────┬───────────┘└──────────────────────┘
             │                           │
             ▼                           ▼
┌────────────────────────┐    ┌──────────────────────┐
│ Skyfield Ephemeris Engine   │ MySQL Database       │
│ (de421.bsp / JPL Data) │    │ (SQLAlchemy ORM)     │
└────────────────────────┘    └──────────────────────┘
```

---

## 🧩 Architectural Components

### 1. Astronomy Engine Layer (`astronomy_engine/`)
* **Domain Models (`core/domain.py`)**: Defines immutable domain data structures (`MoonPhase`, `PlanetPosition`, `SolarState`, `VisibilityWindow`, `Star`, `Constellation`).
* **Engine Orchestration (`core/engine.py`)**: `AstronomyEngine` delegates calculation requests across dedicated service abstractions.
* **Service Interfaces (`services/`)**: Abstract interfaces (`MoonService`, `PlanetService`, `SunService`, `VisibilityService`, `StarService`, `ConstellationService`).
* **Adapters (`implementations/` & `adapters/`)**: `SkyfieldRuntimeAdapter` interfaces with Skyfield ephemeris files (`de421.bsp`) to calculate precise astronomical coordinates.
* **Test Double Factory (`core/factory.py`)**: Provides `create_astronomy_engine(use_stubs=False)`. Setting `use_stubs=True` wires stub implementations (`StubMoonService`, `StubPlanetService`, `StubSunService`, `StubVisibilityService`) as lightweight mock engines for testing.

### 2. Backend Use Case Layer (`backend/use_cases/`)
Coordinates business workflows between the Astronomy Engine, MySQL repositories, and external service adapters:
* `AstronomyUseCase`: Computes real-time sky maps, planetary visibility, and solar/lunar metrics.
* `ObservationPlannerUseCase`: Evaluates observer target scoring and optimal observation windows.
* `LearnUseCase`: Retrieves educational categories, topics, and featured articles from MySQL.
* `EventsUseCase`: Manages upcoming celestial events.
* `NasaApodUseCase`: Retrieves cached NASA Astronomy Picture of the Day entries and triggers background ETL refreshes when needed.

### 3. Database Repository Layer (`database/`)
* **ORM Models (`models.py`)**: Defines SQLAlchemy mappings for 9 tables (`users`, `planets`, `celestial_events`, `educational_categories`, `educational_content`, `observation_logs`, `api_cache`, `application_settings`, `nasa_apod`).
* **Repositories (`repository.py`)**: Generic `SQLAlchemyRepository[T]` providing typed data access methods (`NasaApodRepository`, `EducationalContentRepository`, `CelestialEventRepository`, etc.).
* **Seeding (`seeds.py`)**: Static seeders for reference planets, educational taxonomy, and celestial event schedules.

### 4. ETL Pipeline Framework (`etl/`)
* **Base Contracts (`etl/pipelines/base.py`)**: Abstract `Extractor`, `Transformer`, `Loader`, and `ComposableETLPipeline` contracts.
* **NASA APOD Pipeline (`etl/pipelines/nasa_apod_pipeline.py`)**: Concrete pipeline extracting APOD metadata from NASA API, transforming it into ORM models, and upserting into MySQL.

### 5. Frontend Presentation Layer (`frontend/`)
* Built with Streamlit (`frontend/app.py`).
* Organized into page modules (`frontend/pages/explore.py`, `planner.py`, `discovery.py`).
* Communicates with backend endpoints exclusively via `ApiClient` (`frontend/client.py`).

---

## 📚 Detailed Documentation Links

For deeper technical breakdowns of specific layers, see:
* 📄 [Architecture Overview Deep-Dive](docs/ARCHITECTURE_OVERVIEW.md)
* 🌌 [Astronomy Engine Domain & Architecture](docs/ASTRONOMY_ENGINE_ARCHITECTURE.md)
* 🗄️ [Database Design Specification](DATABASE_DESIGN.md)
* 🔌 [API Endpoint Specification](API_SPECIFICATION.md)
