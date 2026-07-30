# System Architecture

User
    │
    ▼
Frontend (Streamlit)
    │
    ▼
Backend (FastAPI)
    │
    ▼
Astronomy Engine
(Skyfield)
    │
    ├──────────────┐
    ▼              ▼
PostgreSQL     Plotly

---

## Modules

### Astronomy Engine

Responsible for:

- Planet positions
- Moon phases
- Rise and Set calculations
- Astronomical calculations

---

### Explore

Displays

- Visible planets
- Moon phase
- Events

---

### Observation Planner

Calculates

- Observation Window
- Observation Score
- Recommendations

---

### Learn

Provides

- Explanations
- Animations
- Educational Content

---

### Analytics

Displays

- Charts
- Trends
- Dashboards