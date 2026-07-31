# System Architecture

User
    ¦
    ?
Frontend (Streamlit)
    ¦
    ?
Backend (FastAPI)
    ¦
    +---------------------------------------------+
    ?                      ?                      ?
Astronomy Engine        ETL Pipeline          MySQL
(Skyfield)              (Extract / Transform /  SQLAlchemy + Alembic
                        Load)                 Repository Pattern)
    ¦
    ?
Analytics / Visualization
(Plotly)

---

## Modules

### Astronomy Engine

Responsible for:

- Planet positions
- Moon phases
- Rise and set calculations
- Astronomical calculations

### Explore

Displays:

- Visible planets
- Moon phase
- Events

### Observation Planner

Calculates:

- Observation Window
- Observation Score
- Recommendations

### Learn

Provides:

- Explanations
- Animations
- Educational Content

### Analytics

Displays:

- Charts
- Trends
- Dashboards
