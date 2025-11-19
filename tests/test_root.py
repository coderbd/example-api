from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root_default_name() -> None:
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["audience"] == "World"
    assert payload["message"].startswith("Hello, World")


def test_root_custom_name() -> None:
    response = client.get("/", params={"name": "API"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["audience"] == "API"
    assert "API" in payload["message"]


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
