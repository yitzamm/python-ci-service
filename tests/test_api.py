from app.main import create_app


def test_get_vegetables():
    app = create_app()
    client = app.test_client()

    response = client.get("/vegetables")

    assert response.status_code == 200  #  nosec: safe test code
    assert response.json["count"] == 5  #  nosec: safe test code
    assert len(response.json["data"]) == 5  #  nosec: safe test code
