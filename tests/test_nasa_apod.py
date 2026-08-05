"""Tests for NASA APOD adapter, repository, use case, and ETL pipeline."""

from unittest.mock import MagicMock, patch
import pytest

from backend.adapters.nasa_adapter import ApodResult, NasaAdapter, NasaApiConfig
from database.models import NasaApod
from database.repository import NasaApodRepository
from backend.use_cases.nasa_apod_use_case import NasaApodUseCase
from etl.pipelines.nasa_apod_pipeline import ApodExtractor, ApodTransformer, NasaApodPipeline


def test_nasa_adapter_mock_response():
    adapter = NasaAdapter(config=NasaApiConfig(api_key="TEST_KEY"))

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "date": "2026-08-05",
        "title": "Cosmic Pillars",
        "explanation": "Stunning cosmic pillars of dust and gas.",
        "url": "https://apod.nasa.gov/apod/image/test.jpg",
        "media_type": "image",
    }
    mock_response.raise_for_status.return_value = None

    with patch("requests.get", return_value=mock_response):
        result = adapter.get_apod()
        assert result.title == "Cosmic Pillars"
        assert result.apod_date == "2026-08-05"
        assert result.media_type == "image"


def test_apod_transformer():
    transformer = ApodTransformer()
    raw = [
        ApodResult(
            apod_date="2026-08-05",
            title="Pillars of Creation",
            explanation="Deep space view",
            url="https://example.com/image.jpg",
            media_type="image",
        )
    ]
    transformed = transformer.transform(raw)
    assert len(transformed) == 1
    assert isinstance(transformed[0], NasaApod)
    assert transformed[0].title == "Pillars of Creation"
    assert transformed[0].apod_date == "2026-08-05"


def test_apod_use_case():
    mock_repo = MagicMock(spec=NasaApodRepository)
    mock_model = NasaApod(
        apod_date="2026-08-05",
        title="Andromeda Galaxy",
        explanation="Our neighboring galaxy",
        url="https://example.com/andromeda.jpg",
        media_type="image",
    )
    mock_repo.get_by_date.return_value = mock_model
    mock_repo.get_latest.return_value = [mock_model]

    use_case = NasaApodUseCase(apod_repository=mock_repo)

    by_date = use_case.get_by_date("2026-08-05")
    assert by_date is not None
    assert by_date.title == "Andromeda Galaxy"

    recent = use_case.get_recent(limit=5)
    assert len(recent) == 1
    assert recent[0].title == "Andromeda Galaxy"
