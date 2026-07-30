# Astronomy Engine Domain Models

This document defines the stable domain models for the Astronomy Engine.
Each model is shared across the project and represents a clear boundary
between astronomy computations and application layers.

## Location

Purpose:
- Represents the observer's geographic location used for all astronomy calculations.

Fields:
- `latitude`: geographic latitude in decimal degrees.
- `longitude`: geographic longitude in decimal degrees.
- `elevation_meters`: optional elevation above sea level in meters.
- `name`: optional human-readable label for the location.

Why:
- Every astronomy calculation is location-dependent.
- Elevation affects visibility and atmospheric refraction assumptions.
- A name aids debugging and user-facing logging.

Used by:
- All services that compute context-specific astronomy data.

## ObservationContext

Purpose:
- Encapsulates when and where an astronomy request should be evaluated.

Fields:
- `location`: the `Location` of the observer.
- `timestamp`: the instant at which calculations should be performed.
- `timezone`: optional timezone identifier for human-readable formatting.
- `target_objects`: optional list of object names to focus calculations on.

Why:
- Keeps service inputs consistent and reusable.
- Supports object-specific requests without requiring separate argument patterns.

Used by:
- Moon Service, Planet Service, Sun Service, Visibility Service.

## MoonPhase

Purpose:
- Describes the current lunar phase and illumination state.

Fields:
- `phase_name`: e.g. "New Moon" or "Waxing Gibbous".
- `illumination`: fraction of the Moon illuminated, from 0 to 1.
- `phase_angle`: lunar phase angle in degrees.
- `age_days`: optional lunar age in days since new moon.
- `distance_km`: optional current Earth-Moon distance.

Why:
- Moon phase is core to exploration and learning content.
- Phase and illumination are stable, reusable values.

Used by:
- Moon Service, Explore, Learn, and event or planner views that need lunar context.

## MoonVisibility

Purpose:
- Provides rise/set and observable state details for the Moon.

Fields:
- `rise_time`: lunar rise time for the context.
- `set_time`: lunar set time for the context.
- `transit_time`: optional time of meridian transit.
- `altitude_at_transit`: optional altitude at transit.
- `azimuth_rise`: optional azimuth at rise.
- `azimuth_set`: optional azimuth at set.
- `is_visible`: optional boolean indicating whether the Moon is visible.

Why:
- Moon visibility is critical for an observation planner and Explore views.
- Separate from phase to allow the engine to return different lunar concerns independently.

Used by:
- Moon Service, Visibility Service, Observation Planner.

## PlanetPosition

Purpose:
- Represents a planet's celestial coordinates and visibility metadata.

Fields:
- `object_name`: planet name (e.g. "Mars", "Venus").
- `right_ascension`: right ascension in degrees or hours.
- `declination`: declination in degrees.
- `azimuth`: optional azimuth at the observation time.
- `altitude`: optional altitude at the observation time.
- `distance_au`: optional distance from Earth in astronomical units.
- `magnitude`: optional apparent magnitude.
- `is_visible`: optional boolean indicating whether the planet is currently visible.

Why:
- Planetary position is fundamental to Explore and visibility workflows.
- Several fields are optional because some use cases only require coordinates.

Used by:
- Planet Service, Explore, Visibility Service, Observation Planner.

## SolarState

Purpose:
- Describes the Sun's state and daily timing boundaries.

Fields:
- `sunrise`: sunrise time.
- `sunset`: sunset time.
- `solar_noon`: solar noon time.
- `day_length_minutes`: optional day length duration.
- `elevation`: optional solar elevation angle at the timestamp.
- `azimuth`: optional solar azimuth angle at the timestamp.
- `civil_twilight_begin`: optional civil twilight begin time.
- `civil_twilight_end`: optional civil twilight end time.
- `nautical_twilight_begin`: optional nautical twilight begin time.
- `nautical_twilight_end`: optional nautical twilight end time.
- `astronomical_twilight_begin`: optional astronomical twilight begin time.
- `astronomical_twilight_end`: optional astronomical twilight end time.

Why:
- Solar state defines the observation window and dark sky boundaries.
- Twilight times are necessary for planning and analytics.

Used by:
- Sun Service, Visibility Service, Observation Planner.

## VisibilityWindow

Purpose:
- Describes when a celestial object is observable.

Fields:
- `object_name`: the name of the object.
- `start`: start of the visibility window.
- `end`: end of the visibility window.
- `max_elevation`: optional maximum elevation reached during the window.
- `azimuth_at_max`: optional azimuth at maximum elevation.
- `score`: optional convenience score for ranking observation opportunities.
- `description`: optional human-friendly summary.

Why:
- Visibility windows are central to planning and observation workflows.
- They support both raw visibility data and ranked results.

Used by:
- Visibility Service, Observation Planner, Analytics, Explore.

## ObservationScore

Purpose:
- Provides a ranked score for observation opportunities.

Fields:
- `object_name`: the object being scored.
- `score`: normalized numeric score.
- `score_reason`: optional explanation of the score.
- `visibility_window`: optional associated visibility interval.
- `metrics`: optional scoring factor breakdown.

Why:
- A score is necessary for recommendation and ranking use cases.
- The metrics map makes scoring transparent and extensible.

Used by:
- Observation Planner, Visibility Service.

## CelestialEvent

Purpose:
- Models named celestial events such as eclipses, conjunctions, and meteor showers.

Fields:
- `event_id`: optional stable identifier.
- `name`: event name.
- `category`: event category or collection.
- `event_type`: optional type classification.
- `description`: optional narrative description.
- `start_time`: start time of the event.
- `end_time`: optional end time of the event.
- `visibility_window`: optional visibility window for the event.
- `visible_objects`: optional list of objects involved.
- `magnitude`: optional event magnitude or brightness.
- `location`: optional location context, if the event is location-specific.

Why:
- Events are part of exploration and analytics and must be represented consistently.
- This model allows event metadata to be passed through the engine and backend.

Used by:
- Explore, Analytics, event query endpoints, and any event-focused planner flows.
