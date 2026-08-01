"""Unit tests for the Streamlit frontend API client utilities."""

from __future__ import annotations

import pytest
import requests

from frontend.client import ApiClient, ApiClientConfig, FrontendApiError


class _FakeResponse:
    def __init__(self, payload: dict | list | None = None, raise_error: bool = False) -> None:
        self._payload = payload or {}
        self._raise_error = raise_error

    def raise_for_status(self) -> None:
        if self._raise_error:
            raise RuntimeError("boom")

    def json(self) -> dict | list:
        return self._payload


def test_api_client_get_json_returns_decoded_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify the client returns parsed backend JSON for successful requests."""

    def fake_get(url: str, params: dict | None = None, timeout: int = 0) -> _FakeResponse:
        assert url.endswith("/moon")
        assert params["latitude"] == 12.5
        return _FakeResponse(payload={"phase_name": "Full Moon"})

    monkeypatch.setattr("frontend.client.requests.get", fake_get)

    client = ApiClient(config=ApiClientConfig(base_url="http://localhost:8000/api"))
    payload = client.get_moon(latitude=12.5, longitude=77.5)

    assert payload == {"phase_name": "Full Moon"}


def test_api_client_search_city_returns_geocoded_matches(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify city search resolves included geocoded matches for the frontend input workflow."""

    def fake_get(url: str, params: dict | None = None, timeout: int = 0, headers: dict | None = None) -> _FakeResponse:
        assert url == "https://nominatim.openstreetmap.org/search"
        assert params["q"] == "Mumbai"
        return _FakeResponse(payload=[{"display_name": "Mumbai, India", "lat": "19.0760", "lon": "72.8777"}])

    monkeypatch.setattr("frontend.client.requests.get", fake_get)

    client = ApiClient(config=ApiClientConfig(base_url="http://localhost:8000/api"))
    payload = client.search_city("Mumbai")

    assert payload[0]["display_name"] == "Mumbai, India"


def test_api_client_raises_frontend_api_error_on_request_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify request exceptions are surfaced as frontend-friendly errors."""

    def fake_get(url: str, params: dict | None = None, timeout: int = 0) -> _FakeResponse:
        raise requests.RequestException("connection refused")

    monkeypatch.setattr("frontend.client.requests.get", fake_get)

    client = ApiClient(config=ApiClientConfig(base_url="http://localhost:8000/api"))

    with pytest.raises(FrontendApiError):
        client.get_moon(latitude=12.5, longitude=77.5)
