"""Helpers for validating and storing uploaded PDF files.

PDF parsing and text extraction live in ``pdf_loader`` (a later milestone).
Here we only validate that an upload is a PDF and stream it safely to disk
under a size limit, without holding the whole file in memory.
"""

from pathlib import Path

from fastapi import UploadFile

PDF_MAGIC = b"%PDF-"
DEFAULT_CHUNK_SIZE = 1024 * 1024  # 1 MB


class UploadValidationError(Exception):
    """Base class for upload validation failures."""


class InvalidPDFError(UploadValidationError):
    """Raised when the uploaded bytes are not a PDF."""


class EmptyUploadError(UploadValidationError):
    """Raised when the uploaded file has no content."""


class FileTooLargeError(UploadValidationError):
    """Raised when the upload exceeds the configured size limit."""


def sanitize_filename(name: str) -> str:
    """Return a safe display filename with directory components removed.

    Strips both POSIX (``/``) and Windows (``\\``) separators explicitly so
    the result is identical on every platform, then caps the length.
    """
    candidate = name.replace("\x00", "").strip()
    candidate = candidate.replace("\\", "/").rsplit("/", 1)[-1]
    if not candidate:
        return "document.pdf"
    return candidate[:255]


def is_pdf_header(head: bytes) -> bool:
    """Return True if the given bytes start with the PDF magic number."""
    return head.startswith(PDF_MAGIC)


async def stream_upload_to_path(
    file: UploadFile,
    destination: Path,
    max_bytes: int,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> int:
    """Stream an upload to ``destination``, validating type and size.

    Validates the PDF magic number on the first chunk and enforces
    ``max_bytes`` as it reads. Returns the total number of bytes written.

    Raises:
        InvalidPDFError: the first chunk is not a PDF header.
        EmptyUploadError: the upload contained no bytes.
        FileTooLargeError: the upload exceeded ``max_bytes``.
    """
    total = 0
    first_chunk = True
    with destination.open("wb") as buffer:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            if first_chunk:
                if not is_pdf_header(chunk):
                    raise InvalidPDFError("Uploaded file is not a valid PDF.")
                first_chunk = False
            total += len(chunk)
            if total > max_bytes:
                raise FileTooLargeError(
                    "Uploaded file exceeds the maximum allowed size."
                )
            buffer.write(chunk)
    if total == 0:
        raise EmptyUploadError("Uploaded file is empty.")
    return total
