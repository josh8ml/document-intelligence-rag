"""Extract text from PDF files, page by page, using PyMuPDF.

This module turns a stored PDF into a structured ``ExtractedDocument``: a list
of pages, each with its 1-indexed page number, extracted text, and character
count. Downstream milestones clean and chunk this text for embedding.
"""

from pathlib import Path

import pymupdf
from pydantic import BaseModel, Field


class PdfExtractionError(Exception):
    """Raised when a PDF is missing, unreadable, or corrupt."""


class PageText(BaseModel):
    """Text extracted from a single PDF page."""

    page_number: int = Field(description="1-indexed page number.")
    text: str = Field(description="Extracted text for this page.")
    char_count: int = Field(description="Number of characters in the text.")


class ExtractedDocument(BaseModel):
    """The full result of extracting text from a PDF."""

    page_count: int = Field(description="Total number of pages.")
    pages: list[PageText] = Field(description="Per-page extracted text.")
    total_char_count: int = Field(
        description="Sum of character counts across all pages."
    )


def extract_text_from_pdf(path: Path) -> ExtractedDocument:
    """Extract text from a PDF, one page at a time.

    Pages that contain no embedded text (for example, image-only scans) yield
    an empty string rather than raising; the surrounding pages are unaffected.

    Args:
        path: Filesystem path to the PDF.

    Returns:
        An ``ExtractedDocument`` with per-page text and page numbers.

    Raises:
        PdfExtractionError: The file is missing, unreadable, or not a valid PDF.
    """
    if not path.exists():
        raise PdfExtractionError(f"File not found: {path}")

    pages: list[PageText] = []
    total_chars = 0

    try:
        with pymupdf.open(str(path)) as document:
            for index in range(document.page_count):
                page = document.load_page(index)
                text = page.get_text()
                char_count = len(text)
                total_chars += char_count
                pages.append(
                    PageText(
                        page_number=index + 1,
                        text=text,
                        char_count=char_count,
                    )
                )
    except (RuntimeError, OSError, ValueError) as exc:
        raise PdfExtractionError(f"Could not read PDF: {path}") from exc

    return ExtractedDocument(
        page_count=len(pages),
        pages=pages,
        total_char_count=total_chars,
    )
