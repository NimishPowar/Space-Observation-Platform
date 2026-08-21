# Database Design & Schema Specification

The database uses MySQL with SQLAlchemy ORM mappings and Alembic migrations. Dynamic ephemeris calculations (planet coordinates, sky maps, solar twilight) are computed on demand by the Astronomy Engine (Skyfield), while reusable reference data, educational topics, cached APOD metadata, and user logs are persisted.

---

## 🗄️ Relational Schema & Tables

### 1. `users`
Stores user accounts for authentication and personal settings.
- `id` (INT, PK, Auto-Increment)
- `username` (VARCHAR(64), Unique, Indexed)
- `email` (VARCHAR(255), Unique, Indexed)
- `hashed_password` (VARCHAR(255))
- `is_active` (BOOLEAN, Default True)
- `created_at`, `updated_at` (DATETIME)

### 2. `planets`
Stores static reference metrics for solar system planets.
- `id` (INT, PK, Auto-Increment)
- `name` (VARCHAR(64), Unique, Indexed) — e.g. `mars`, `jupiter`
- `display_name` (VARCHAR(128))
- `category` (VARCHAR(64)) — e.g. `terrestrial`, `gas_giant`
- `description` (TEXT)
- `mass_kg`, `radius_km`, `semi_major_axis_au`, `orbital_period_days`, `mean_density_g_cm3` (FLOAT)
- `source_url` (TEXT)
- `created_at`, `updated_at` (DATETIME)

### 3. `celestial_events`
Stores upcoming celestial events (meteor showers, conjunctions, oppositions).
- `id` (INT, PK, Auto-Increment)
- `event_type` (VARCHAR(64))
- `title` (VARCHAR(255))
- `description` (TEXT)
- `starts_at` (DATETIME, Indexed)
- `ends_at` (DATETIME)
- `source_url` (TEXT)
- `is_recurring` (BOOLEAN, Default False)
- `planet_id` (INT, FK → `planets.id`)
- `created_at`, `updated_at` (DATETIME)

### 4. `educational_categories`
Taxonomy categories for Astronomy Basics content.
- `id` (INT, PK, Auto-Increment)
- `name` (VARCHAR(128), Unique)
- `slug` (VARCHAR(128), Unique, Indexed)
- `description` (TEXT)
- `created_at`, `updated_at` (DATETIME)

### 5. `educational_content`
Detailed educational articles and astronomy topics.
- `id` (INT, PK, Auto-Increment)
- `category_id` (INT, FK → `educational_categories.id`)
- `title` (VARCHAR(255))
- `slug` (VARCHAR(128), Unique, Indexed)
- `excerpt` (TEXT)
- `body` (TEXT)
- `source_url` (TEXT)
- `is_featured` (BOOLEAN, Default False)
- `created_at`, `updated_at` (DATETIME)

### 6. `nasa_apod`
Cached entries from the NASA Astronomy Picture of the Day API.
- `id` (INT, PK, Auto-Increment)
- `apod_date` (VARCHAR(10), Unique, Indexed) — `YYYY-MM-DD`
- `title` (VARCHAR(500))
- `explanation` (TEXT)
- `url` (TEXT)
- `hdurl` (TEXT)
- `media_type` (VARCHAR(32))
- `copyright_text` (VARCHAR(500))
- `thumbnail_url` (TEXT)
- `source_api` (VARCHAR(64), Default `nasa_apod`)
- `created_at`, `updated_at` (DATETIME)

### 7. `observation_logs`
User observation session notes and telescope logs.
- `id` (INT, PK, Auto-Increment)
- `user_id` (INT, FK → `users.id`)
- `celestial_event_id` (INT, FK → `celestial_events.id`, Optional)
- `target_name` (VARCHAR(128))
- `observation_time` (DATETIME)
- `rating` (INT)
- `notes` (TEXT)
- `created_at`, `updated_at` (DATETIME)

### 8. `api_cache`
System caching table for external API payloads.
- `id` (INT, PK, Auto-Increment)
- `cache_key` (VARCHAR(255), Unique, Indexed)
- `response_json` (TEXT)
- `expires_at` (DATETIME, Indexed)
- `created_at`, `updated_at` (DATETIME)

### 9. `application_settings`
System and user preference settings.
- `id` (INT, PK, Auto-Increment)
- `user_id` (INT, FK → `users.id`, Optional)
- `setting_key` (VARCHAR(128), Indexed)
- `setting_value` (TEXT)
- `created_at`, `updated_at` (DATETIME)