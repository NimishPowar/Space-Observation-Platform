"""Unit & integration tests for sky map, stars, and constellation services and API endpoints."""

from datetime import datetime, timezone
from fastapi.testclient import TestClient

from astronomy_engine.core.domain import Location, ObservationContext
from astronomy_engine.core.factory import create_astronomy_engine
from astronomy_engine.services.star_service import DefaultStarService
from astronomy_engine.services.constellation_service import DefaultConstellationService
from backend.api.main import app


def test_star_service_calculations():
    context = ObservationContext(
        location=Location(latitude=51.5, longitude=-0.1),  # London
        timestamp=datetime(2026, 8, 5, 22, 0, 0, tzinfo=timezone.utc),
    )
    star_service = DefaultStarService()
    stars = star_service.list_visible_stars(context, min_altitude=-90.0)

    assert len(stars) > 0
    star_names = [s.name for s in stars]
    assert "Vega" in star_names or "Polaris" in star_names
    for star in stars:
        assert star.altitude is not None
        assert star.azimuth is not None
        assert star.magnitude is not None


def test_constellation_service_calculations():
    context = ObservationContext(
        location=Location(latitude=51.5, longitude=-0.1),
        timestamp=datetime(2026, 8, 5, 22, 0, 0, tzinfo=timezone.utc),
    )
    const_service = DefaultConstellationService()
    constellations = const_service.list_constellations(context)

    assert len(constellations) > 0
    const_names = [c.name for c in constellations]
    assert "Ursa Major (Big Dipper)" in const_names or "Cassiopeia" in const_names


def test_astronomy_engine_skymap():
    engine = create_astronomy_engine()
    context = ObservationContext(
        location=Location(latitude=12.5, longitude=77.5),
        timestamp=datetime(2026, 8, 5, 20, 0, 0, tzinfo=timezone.utc),
    )
    skymap = engine.get_skymap_data(context)

    assert skymap.moon is not None
    assert skymap.sun is not None
    assert isinstance(skymap.planets, list)
    assert len(skymap.stars) > 0
    assert len(skymap.constellations) > 0


def test_api_stars_endpoint():
    client = TestClient(app)
    response = client.get("/api/stars", params={"latitude": 12.5, "longitude": 77.5})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert "altitude" in data[0]


def test_api_constellations_endpoint():
    client = TestClient(app)
    response = client.get("/api/constellations", params={"latitude": 12.5, "longitude": 77.5})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "lines" in data[0]


def test_api_skymap_endpoint():
    client = TestClient(app)
    response = client.get("/api/skymap", params={"latitude": 12.5, "longitude": 77.5})
    assert response.status_code == 200
    data = response.json()
    assert "moon" in data
    assert "planets" in data
    assert "stars" in data
    assert "constellations" in data
