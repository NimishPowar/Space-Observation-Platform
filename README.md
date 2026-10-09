# 🌌 Space Observation Intelligence Platform

> Explore · Plan · Discover · Analyze

## Overview

The **Space Observation Intelligence Platform** is a data-driven web application built with Clean Architecture that enables astronomy enthusiasts and researchers to discover visible celestial objects, plan observation sessions with calculated visibility scoring, explore interactive 3D solar system models, and analyze observation telemetry through a dedicated analytics dashboard.

The project combines Astronomy Calculations (Skyfield), FastAPI backend REST endpoints, MySQL/SQLite persistence via SQLAlchemy, an automated NASA APOD ETL pipeline, and an interactive Streamlit frontend with Plotly analytics and Three.js WebGL 3D visualizations.

---

## 🚀 Key Features & Modules

- 🌟 **Explore Night Sky**:
  - Real-time sky map displaying visible planetary positions, bright star catalogs, and constellation line connections.
  - Precise observer topocentric coordinates, solar twilight boundaries (civil, nautical, astronomical), and real-time lunar position.

- 🔭 **Observation Planner**:
  - Target visibility scoring algorithm based on topocentric altitude, minimum elevation cutoffs, and solar/lunar interference.
  - Customizable observation time windows and tracking of upcoming celestial events (e.g., meteor showers, planetary conjunctions, eclipses).

- 📊 **Analytics Dashboard**:
  - Real-time target suitability scores ($0–100\%$) and priority ranking table.
  - Dynamic Plotly target distribution donut charts categorized by object class (*Terrestrial Planets*, *Gas Giants*, *Lunar*, *Deep-Sky & Other*).
  - 24-hour hourly elevation trajectory curves for key celestial bodies (Venus, Mars, Jupiter, Saturn, Moon).
  - System telemetry metrics displaying active target counts, average suitability scores, top observable target, and logged observation statistics.

- 💡 **Discovery & 3D Interactive Modules**:
  - **Astronomy Knowledge Base**: Searchable topic library across 8 astronomical domains (*Solar System, Stars, Galaxies, Nebulae, Black Holes, Exoplanets, Comets, Asteroids*) stored in persistent database models.
  - **3D Solar System View**: Interactive WebGL 3D orbital simulation built with Three.js featuring real-time speed controls and date/time tracking.
  - **3D Moon Phase Simulator**: Physically driven 3D Earth-Moon directional lighting model paired with calculated illumination percentages, lunar age, phase angle, and rise/set timing.
  - **NASA APOD Gallery**: Interactive Astronomy Picture of the Day viewer featuring date selectors, HD resolution image modals, and full explanation details.

- 🖼️ **NASA APOD & ETL Pipeline**:
  - Extensible Extract-Transform-Load (ETL) pipeline infrastructure (`BaseETLPipeline`, `Extractor`, `Transformer`, `Loader`).
  - Automated caching of NASA's Astronomy Picture of the Day into database storage with API fallback support.

---

## 🛠️ Technology Stack

- **Language**: Python 3.10+
- **Backend API**: FastAPI, Uvicorn, Pydantic v2
- **Frontend UI**: Streamlit, Plotly, Three.js WebGL (via HTML components)
- **Database & ORM**: MySQL / SQLite, SQLAlchemy 2.0, Alembic
- **Astronomy Engine**: Skyfield, NumPy, SciPy (JPL Ephemeris kernel `de421.bsp`)
- **ETL & Integration**: Requests, python-dotenv, Pytest

---

## 📋 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/NimishPowar/Space-Observation-Platform.git
cd "Space Observation Platform"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the example environment configuration file to `.env` and fill in your database credentials and NASA API key:
```bash
cp .env.example .env
```
Example `.env`:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_NAME=space_observation_platform
DB_USER=root
DB_PASSWORD=YourPasswordHere
NASA_API_KEY=YourNasaApiKeyHere
```

### 4. Database Setup & Migrations
Ensure your database server is running and the database exists. Run Alembic migrations and seed initial reference data:
```bash
# Run Alembic migrations
alembic upgrade head

# Seed initial reference data (planets, topics, celestial events)
python -c "from database.session import DatabaseSessionManager; from database.seeds import seed_reference_data; seed_reference_data(DatabaseSessionManager().get_session())"
```

---

## 🏃 Running the Application

### 1. Start the FastAPI Backend Server (Terminal 1)
```bash
uvicorn backend.api.main:app --reload --port 8000
```
*Interactive API Documentation available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

### 2. Start the Streamlit Frontend App (Terminal 2)
```bash
streamlit run frontend/app.py
```
*User Interface available at [http://localhost:8501](http://localhost:8501)*

---

## 🧪 Automated Testing

Run the full unit and API integration test suite with `pytest`:
```bash
pytest
```
*All 38 test suites cover astronomy engine calculations, database repositories, API endpoints, ETL pipelines, and analytics modules.*
