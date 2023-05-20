from app import app


def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_render_most_popular_not_found():
    client = app.test_client()
    response = client.get("/most-popular/invalid")
    assert response.status_code == 404
