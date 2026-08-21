# API Specification

Base Path: `/api`

---

## 🌌 Astronomy Engine Endpoints (Live Ephemeris Calculations)

### `GET /api/moon`
Returns lunar phase, illumination, phase angle, and rise/set visibility.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)

---

### `GET /api/planets`
Returns positions (altitude, azimuth, RA, declination, distance, visibility) for planets.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)
  - `names` (list of strings, optional)

---

### `GET /api/sun`
Returns solar state, sunrise, sunset, solar noon, and twilight boundaries.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)

---

### `GET /api/stars`
Returns visible star positions for sky mapping.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)
  - `min_altitude` (float, optional, default `0.0`)
  - `max_magnitude` (float, optional, default `6.0`)
  - `limit` (int, optional, default `500`)

---

### `GET /api/constellations`
Returns constellation line segments and star connectivity for sky mapping.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)

---

### `GET /api/skymap`
Combined payload of stars and constellation line connections for sky maps.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)

---

### `GET /api/visibility`
Returns computed observation visibility windows for requested objects.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)
  - `names` (list of strings, optional)

---

### `GET /api/planner`
Evaluates target visibility scores and computes optimal observation windows.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `elevation` (float, optional, default `0.0`)
  - `target_names` (list of strings, optional)
  - `min_altitude` (float, optional, default `15.0`)

---

## 🖼️ NASA APOD Endpoints

### `GET /api/apod/today`
Returns today's NASA Astronomy Picture of the Day (auto-fetches via ETL if missing).

### `GET /api/apod/recent`
Returns recent APOD entries from MySQL.
- **Query Parameters**: `limit` (int, default `10`)

### `GET /api/apod/{target_date}`
Returns APOD entry for a specific date (`YYYY-MM-DD`).

---

## 💡 Discovery Hub Endpoints

### `GET /api/discovery/categories`
Returns list of educational taxonomy categories.

### `GET /api/discovery/topics`
Searches Astronomy Basics educational topics.
- **Query Parameters**:
  - `query` (string, optional)
  - `category` (string, optional, slug)
  - `limit` (int, default `50`)

### `GET /api/discovery/featured`
Returns featured educational articles.

### `GET /api/discovery/topic/{slug}`
Returns detailed educational article by slug.

### `GET /api/discovery/moon-phase`
Returns calculated lunar phase statistics for the Moon Phase Simulator.
- **Query Parameters**:
  - `timestamp` (string, optional, ISO-8601)
  - `day_offset` (int, optional, default `0`)

---

## 📅 Reference Data Endpoints

### `GET /api/events`
Returns upcoming celestial events from MySQL ordered by start time.
- **Query Parameters**:
  - `latitude` (float, required)
  - `longitude` (float, required)
  - `timestamp` (string, optional, ISO-8601)
  - `limit` (int, default `50`)

### `GET /api/learn/{object_name}`
Returns educational content for an object name or slug.
