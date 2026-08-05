"""Unit tests for upload validation helpers."""

from app.ingestion.upload import is_pdf_header, sanitize_filename


def test_sanitize_strips_posix_directory_components() -> None:
    assert sanitize_filename("../../etc/passwd") == "passwd"


def test_sanitize_strips_windows_directory_components() -> None:
    assert sanitize_filename("C:\\Users\\me\\report.pdf") == "report.pdf"


def test_sanitize_defaults_when_empty() -> None:
    assert sanitize_filename("   ") == "document.pdf"


def test_is_pdf_header_accepts_pdf_bytes() -> None:
    assert is_pdf_header(b"%PDF-1.7 rest of file") is True


def test_is_pdf_header_rejects_other_bytes() -> None:
    assert is_pdf_header(b"PK\x03\x04 zip archive") is False
