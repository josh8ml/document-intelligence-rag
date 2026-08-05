"""Integration tests for the document upload endpoint."""

import io
from pathlib import Path

from app.core.config import Settings, get_settings
from app.main import create_app
from fastapi.testclient import TestClient

VALID_PDF = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def _make_client(tmp_path: Path, max_mb: int = 25) -> TestClient:
    """Build a TestClient whose uploads go to a temporary directory."""
    application = create_app()

    def _override_settings() -> Settings:
        return Settings(upload_dir=str(tmp_path), max_upload_size_mb=max_mb)

    application.dependency_overrides[get_settings] = _override_settings
    return TestClient(application)


def test_upload_valid_pdf_returns_metadata(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    files = {"file": ("report.pdf", io.BytesIO(VALID_PDF), "application/pdf")}
    response = client.post("/documents/upload", files=files)

    assert response.status_code == 201
    body = response.json()
    assert body["filename"] == "report.pdf"
    assert body["stored_filename"].endswith(".pdf")
    assert body["size_bytes"] == len(VALID_PDF)
    assert (tmp_path / body["stored_filename"]).exists()


def test_upload_rejects_non_pdf_extension(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    files = {"file": ("notes.txt", io.BytesIO(b"hello"), "text/plain")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 400


def test_upload_rejects_pdf_extension_with_bad_content(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    files = {"file": ("fake.pdf", io.BytesIO(b"not a pdf"), "application/pdf")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 400
    assert list(tmp_path.glob("*.pdf")) == []


def test_upload_rejects_empty_file(tmp_path: Path) -> None:
    client = _make_client(tmp_path)
    files = {"file": ("empty.pdf", io.BytesIO(b""), "application/pdf")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 400
    assert list(tmp_path.glob("*.pdf")) == []


def test_upload_rejects_oversized_file(tmp_path: Path) -> None:
    client = _make_client(tmp_path, max_mb=1)
    big = b"%PDF-1.4\n" + b"0" * 1_200_000
    files = {"file": ("big.pdf", io.BytesIO(big), "application/pdf")}
    response = client.post("/documents/upload", files=files)
    assert response.status_code == 413
    assert list(tmp_path.glob("*.pdf")) == []
