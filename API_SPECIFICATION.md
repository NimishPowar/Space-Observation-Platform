# API Specification

Base path: `/api`

## Astronomy (live calculations via Astronomy Engine)

### GET /moon

Returns moon phase information for a location and timestamp.

Query parameters:

- `latitude` (required)
- `longitude` (required)
- `timestamp` (optional, ISO-8601)
- `elevation` (optional, meters)

---

### GET /planets

Returns visible planetary positions for a location and timestamp.

Query parameters:

- `latitude` (required)
- `longitude` (required)
- `timestamp` (optional, ISO-8601)
- `elevation` (optional, meters)
- `names` (optional, repeated query parameter)

---

### GET /sun

Returns solar state for a location and timestamp.

Query parameters:

- `latitude` (required)
- `longitude` (required)
- `timestamp` (optional, ISO-8601)
- `elevation` (optional, meters)

---

### GET /visibility

Returns visibility windows for requested objects.

Query parameters:

- `latitude` (required)
- `longitude` (required)
- `timestamp` (optional, ISO-8601)
- `elevation` (optional, meters)
- `names` (optional, repeated query parameter)

---

## Reference Data (MySQL-backed)

### GET /events

Returns upcoming celestial events from the database, ordered by start time.

Query parameters:

- `latitude` (required; reserved for future location-aware filtering)
- `longitude` (required; reserved for future location-aware filtering)
- `timestamp` (optional, ISO-8601; defaults to current UTC)
- `limit` (optional, default `50`, max `200`)

Response fields:

- `event_id`
- `name`
- `category`
- `event_type`
- `description`
- `start_time`
- `end_time`
- `visible_objects`
- `magnitude`
- `location`

---

### GET /learn/{object_name}

Returns educational content for an object name or slug from the database.

Path parameters:

- `object_name` — slug (for example `mars-overview`) or resolvable object name (for example `mars`)

Response fields:

- `object_name`
- `slug`
- `title`
- `excerpt`
- `body`
- `category_slug`
- `category_name`
- `source_url`
- `is_featured`

Returns `404` when no matching educational content exists.

---

## Analytics

### GET /analytics

Returns dashboard data.

Status: not implemented yet.
