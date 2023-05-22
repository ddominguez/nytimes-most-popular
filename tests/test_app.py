import pytest
import requests

from mostpopular import create_app
from mostpopular.constants import LIST_TYPES
from mostpopular.utils import fetch_most_popular


@pytest.fixture
def app():
    app = create_app({"CACHE_TYPE": "NullCache", "NYT_API_KEY": "fake"})
    return app


# https://docs.pytest.org/en/7.3.x/how-to/monkeypatch.html#monkeypatching-returned-objects-building-mock-classes
class MockResponse:
    @staticmethod
    def json():
        return {"results": []}

    @staticmethod
    def raise_for_status():
        pass


@pytest.fixture
def mock_most_popular(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)


def test_fetch_most_popular(app, mock_most_popular):
    results = fetch_most_popular(app.config.get("NYT_API_KEY"), "emailed")
    assert "results" in results


def test_index_request(app):
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "test_param,expected", [(t, 200) for t in LIST_TYPES] + [("bad", 404)]
)
def test_render_most_popular_request(app, mock_most_popular, test_param, expected):
    client = app.test_client()
    response = client.get(f"/most-popular/{test_param}")
    assert response.status_code == expected
