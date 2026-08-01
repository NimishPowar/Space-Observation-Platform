import requests

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiClientConfig:
    """Configuration for talking to the backend API."""

    base_url: str = "http://127.0.0.1:8000/api"
    timeout_seconds: int = 10


class FrontendApiError(RuntimeError):
    """Raised when a backend request fails."""


class ApiClient:
    """Small reusable client for the backend astronomy endpoints."""

    def __init__(self, config: ApiClientConfig | None = None) -> None:
        self._config = config or ApiClientConfig()

    def get_json(self, path: str, params: dict | None = None) -> dict | list:
        """Return JSON from a backend endpoint or raise a user-friendly error."""
        try:
            response = requests.get(
                f"{self._config.base_url}{path}",
                params=params,
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise FrontendApiError(f"Unable to reach the backend API: {exc}") from exc

        try:
            return response.json()
        except ValueError as exc:
            raise FrontendApiError("The backend returned an invalid JSON response.") from exc

    def search_city(self, query: str) -> list[dict]:
        """Resolve a city query into a small list of geocoded coordinates."""
        cleaned_query = query.strip()
        if not cleaned_query:
            raise FrontendApiError("Enter a city name to search.")

        try:
            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": cleaned_query,
                    "format": "jsonv2",
                    "limit": 5,
                    "addressdetails": 1,
                },
                headers={"User-Agent": "SpaceObservationPlatform/1.0"},
                timeout=self._config.timeout_seconds,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise FrontendApiError(f"Unable to resolve the city search request: {exc}") from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise FrontendApiError("The city search service returned an invalid response.") from exc

        if not isinstance(payload, list) or not payload:
            raise FrontendApiError(f"No city matches were found for '{cleaned_query}'.")

        return payload

    def get_moon(self, latitude: float, longitude: float, timestamp: str | None = None, elevation: float | None = None) -> dict:
        return self.get_json(
            "/moon",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "elevation": elevation,
            },
        )

    def get_planets(self, latitude: float, longitude: float, timestamp: str | None = None, elevation: float | None = None, names: list[str] | None = None) -> list:
        return self.get_json(
            "/planets",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "elevation": elevation,
                "names": names,
            },
        )

    def get_sun(self, latitude: float, longitude: float, timestamp: str | None = None, elevation: float | None = None) -> dict:
        return self.get_json(
            "/sun",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "elevation": elevation,
            },
        )

    def get_visibility(self, latitude: float, longitude: float, timestamp: str | None = None, elevation: float | None = None, names: list[str] | None = None) -> list:
        return self.get_json(
            "/visibility",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "elevation": elevation,
                "names": names,
            },
        )

    def get_planner(self, latitude: float, longitude: float, timestamp: str | None = None, elevation: float | None = None, names: list[str] | None = None, limit: int = 5) -> list:
        return self.get_json(
            "/planner",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "elevation": elevation,
                "names": names,
                "limit": limit,
            },
        )

    def get_events(
        self,
        latitude: float = 12.5,
        longitude: float = 77.5,
        timestamp: str | None = None,
        limit: int = 10,
    ) -> list:
        return self.get_json(
            "/events",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "timestamp": timestamp,
                "limit": limit,
            },
        )

    def get_learn(self, object_name: str) -> dict:
        return self.get_json(
            f"/learn/{object_name.strip().lower()}",
        )
