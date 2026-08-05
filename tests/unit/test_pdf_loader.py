"""Unit tests for PDF text extraction.

Fixtures are generated in code with PyMuPDF, so no binary files are committed
to the repository. Each test builds a small PDF in a temporary directory.
"""

from pathlib import Path

import pymupdf
import pytest
from app.ingestion.pdf_loader import (
    ExtractedDocument,
    PdfExtractionError,
    extract_text_from_pdf,
)


def _write_pdf(path: Path, pages: list[str]) -> None:
    """Create a PDF at ``path`` with one page per string in ``pages``."""
    document = pymupdf.open()
    try:
        for content in pages:
            page = document.new_page()
            page.insert_text((72, 72), content)
        document.save(str(path))
    finally:
        document.close()


def test_extracts_text_per_page(tmp_path: Path) -> None:
    pdf_path = tmp_path / "doc.pdf"
    _write_pdf(pdf_path, ["Hello from page one", "Second page content"])

    result = extract_text_from_pdf(pdf_path)

    assert isinstance(result, ExtractedDocument)
    assert result.page_count == 2
    assert len(result.pages) == 2
    assert "Hello from page one" in result.pages[0].text
    assert "Second page content" in result.pages[1].text


def test_preserves_page_numbers(tmp_path: Path) -> None:
    pdf_path = tmp_path / "doc.pdf"
    _write_pdf(pdf_path, ["a", "b", "c"])

    result = extract_text_from_pdf(pdf_path)

    assert [page.page_number for page in result.pages] == [1, 2, 3]


def test_char_counts_are_consistent(tmp_path: Path) -> None:
    pdf_path = tmp_path / "doc.pdf"
    _write_pdf(pdf_path, ["some text here", "more"])

    result = extract_text_from_pdf(pdf_path)

    for page in result.pages:
        assert page.char_count == len(page.text)
    assert result.total_char_count == sum(p.char_count for p in result.pages)


def test_missing_file_raises() -> None:
    with pytest.raises(PdfExtractionError):
        extract_text_from_pdf(Path("does/not/exist.pdf"))


def test_corrupt_pdf_raises(tmp_path: Path) -> None:
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"this is definitely not a valid pdf file")

    with pytest.raises(PdfExtractionError):
        extract_text_from_pdf(bad)
