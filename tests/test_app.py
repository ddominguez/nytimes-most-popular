import pytest
import requests

from app import app, fetch_most_popular, LIST_TYPES


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
    monkeypatch.setitem(app.config, "NYT_API_KEY", "fake")


def test_fetch_most_popular(mock_most_popular):
    results = fetch_most_popular("emailed")
    assert "results" in results


def test_index_request():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


# @pytest.mark.skip()
@pytest.mark.parametrize(
    "test_param,expected", [(t, 200) for t in LIST_TYPES] + [("bad", 404)]
)
def test_render_most_popular_request(mock_most_popular, test_param, expected):
    client = app.test_client()
    response = client.get(f"/most-popular/{test_param}")
    assert response.status_code == expected
