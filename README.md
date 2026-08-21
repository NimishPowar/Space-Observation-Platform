# 🌌 Space Observation Intelligence Platform

> Explore · Plan · Discover

## Overview

The **Space Observation Intelligence Platform** is a data-driven web application built with Clean Architecture that enables users to discover visible celestial objects, plan observation sessions with calculated visibility scoring, and explore interactive 3D astronomy modules.

The project combines Astronomy Calculations (Skyfield), FastAPI backend endpoints, MySQL persistence, an automated NASA APOD ETL pipeline, and an interactive Streamlit frontend.

---

## Implemented Modules & Features

- 🌟 **Explore**: Real-time night sky map, visible planetary positions, bright stars, constellation line connectivity, solar twilight boundaries, and lunar state.
- 🔭 **Observation Planner**: Target visibility scoring, custom observation windows, and upcoming celestial event tracking.
- 💡 **Discovery**:
  - **Astronomy Basics**: Searchable knowledge base across 8 astronomical topics (*Solar System, Stars, Galaxies, Nebulae, Black Holes, Exoplanets, Comets, Asteroids*) stored in MySQL.
  - **3D Solar System View**: Interactive WebGL 3D orbit visualization with speed controls and simulated clock.
  - **3D Moon Phase Simulator**: Physically-driven 3D Earth-Moon directional lighting model paired with calculated illumination, lunar age, phase angle, and rise/set timing.
- 🖼️ **NASA APOD & ETL**: Automated Extract-Transform-Load (ETL) pipeline that caches NASA's Astronomy Picture of the Day into MySQL for daily presentation.

---

## Technology Stack

- **Language**: Python 3.10+
- **Backend API**: FastAPI, Uvicorn, Pydantic
- **Frontend**: Streamlit, Three.js WebGL embeds
- **Database & ORM**: MySQL, SQLAlchemy, Alembic
- **Astronomy Engine**: Skyfield, NumPy, SciPy
- **ETL & Data Handling**: Requests, python-dotenv

---

## Getting Started

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
DB_PASSWORD=YourPassword Here
NASA_API_KEY=YourNasaApiKeyHere
```

### 4. Database Setup & Migrations
Ensure your MySQL server is running and the database `space_observation_platform` exists. Run database migrations and seed reference data:
```bash
# Run Alembic migrations
alembic upgrade head

# Seed initial reference data (planets, topics, celestial events)
python -c "from database.session import DatabaseSessionManager; from database.seeds import seed_reference_data; seed_reference_data(DatabaseSessionManager().get_session())"
```

### 5. Launch the Application

#### Start the FastAPI Backend Server (Terminal 1)
```bash
uvicorn backend.api.main:app --reload --port 8000
```
*API Swagger Documentation available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

#### Start the Streamlit Frontend App (Terminal 2)
```bash
streamlit run frontend/app.py
```
*User Interface available at [http://localhost:8501](http://localhost:8501)*

---

## Testing

Run the automated test suite with `pytest`:
```bash
pytest
```
