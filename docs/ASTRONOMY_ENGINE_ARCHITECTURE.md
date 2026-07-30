# Astronomy Engine Architecture

This document describes the designed architecture for the Astronomy Engine
in the Space Observation Intelligence Platform. The engine is intentionally
independent from FastAPI and Streamlit and is built as a domain-focused,
service-oriented layer.

## Architectural Principles

- The Astronomy Engine is a standalone Python package.
- It exposes clean service interfaces to the backend.
- It encapsulates Skyfield behind adapters so the rest of the application never
  depends directly on Skyfield-specific types.
- Service responsibilities are separated by celestial domain concerns.
- The backend communicates with the engine through a small orchestrator API.

## Package Structure

- `astronomy_engine/core`
  - Domain models and engine orchestration.
  - Contains the public `AstronomyEngine` entrypoint.

- `astronomy_engine/services`
  - Abstract service interfaces for moon, planet, sun, and visibility behavior.
  - Defines the public engine contract.

- `astronomy_engine/adapters`
  - External integration adapters.
  - Contains Skyfield-specific adapter interfaces and future adapter
    implementations.

- `astronomy_engine/calculations`
  - Calculation placeholders and helper routines.
  - Supports the engine internals without exposing logic externally.

## Service Responsibilities

### Moon Service

Responsibilities:
- Provide the current moon phase name and illumination.
- Expose lunar rise and set times.
- Return moon-specific visibility details for a given location/time.

Public interface:
- `get_moon_phase(context: ObservationContext) -> MoonPhase`
- `get_lunar_visibility(context: ObservationContext) -> MoonPhase`

### Planet Service

Responsibilities:
- Provide planetary positions and visibility metadata.
- List visible planets for a location and time.
- Return position data for an individual planet by name.

Public interface:
- `list_visible_planets(context: ObservationContext) -> list[PlanetPosition]`
- `get_planet_position(name: str, context: ObservationContext) -> PlanetPosition`

### Sun Service

Responsibilities:
- Provide sunrise and sunset times.
- Provide solar state information such as solar noon, elevation, and azimuth.

Public interface:
- `get_solar_state(context: ObservationContext) -> SolarState`
- `get_sunrise_sunset(context: ObservationContext) -> SolarState`

### Visibility Service

Responsibilities:
- Compute visibility windows for celestial objects.
- Rank or prioritize observation windows.
- Determine whether a given object is visible in a context.

Public interface:
- `compute_visibility(context: ObservationContext, object_names: Optional[list[str]] = None) -> list[VisibilityWindow]`
- `compute_best_observation_windows(context: ObservationContext, object_names: Optional[list[str]] = None) -> list[VisibilityWindow]`
- `is_object_visible(object_name: str, context: ObservationContext) -> bool`

## Backend Communication

The backend should communicate with the Astronomy Engine through the
`AstronomyEngine` orchestrator in `astronomy_engine.core.engine`.

The backend composition root (for example, application startup) will create
concrete service implementations and instantiate `AstronomyEngine` with them.
The backend then uses engine methods such as:

- `get_moon_summary(context)`
- `get_planetary_positions(context)`
- `get_solar_summary(context)`
- `get_visibility_windows(context, object_names)`
- `get_best_observation_windows(context, object_names)`

This keeps the backend decoupled from service implementation details and
ensures the engine remains framework-agnostic.

## Skyfield Encapsulation

Skyfield must be contained entirely within the astronomy engine's adapter layer.
Concrete adapters will implement an abstract `SkyfieldAdapter` interface.

The rest of the project should only depend on:

- `astronomy_engine.services` service interfaces
- `astronomy_engine.core.domain` models
- `AstronomyEngine` orchestrator methods

No FastAPI route, Streamlit component, or backend use case should import
Skyfield directly.

By encapsulating Skyfield behind adapters:
- the engine can be tested without Skyfield.
- Skyfield can be replaced if required.
- external layers remain clean and stable.

## Design Summary

This architecture defines a clear boundary between:
- the public engine contract (`services` and `core`)
- the concrete astronomy implementation (`adapters` and `calculations`)
- the external application layers (backend and frontend)

The engine is intentionally designed to be independent, testable, and easy to
grow as astronomy requirements expand.
