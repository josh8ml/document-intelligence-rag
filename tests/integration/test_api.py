"""Integration tests for the FastAPI application via TestClient.

These call the application the way a client would — over HTTP through
``TestClient`` — so they catch routing, dependency, and serialization issues,
not just function-level logic.
"""

from app import __version__
from app.main import create_app
from fastapi.testclient import TestClient

client = TestClient(create_app())


def test_health_endpoint_reports_ok() -> None:
    """The health endpoint returns 200 with a status of 'ok'."""
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["app_name"]
    assert body["environment"]


def test_version_endpoint_matches_package() -> None:
    """The version endpoint reports the installed package version."""
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == __version__


def test_root_endpoint_points_to_docs() -> None:
    """The root endpoint returns service info and the docs path."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs_url"] == "/docs"


def test_openapi_docs_available() -> None:
    """The interactive Swagger UI is served."""
    response = client.get("/docs")
    assert response.status_code == 200
