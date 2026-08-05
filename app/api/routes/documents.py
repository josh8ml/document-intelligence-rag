"""Document management endpoints.

Currently exposes upload. Extraction, listing, search, and deletion arrive in
later milestones.
"""

from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import Settings, get_settings
from app.ingestion.upload import (
    EmptyUploadError,
    FileTooLargeError,
    InvalidPDFError,
    sanitize_filename,
    stream_upload_to_path,
)
from app.models.schemas import UploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])

SettingsDep = Annotated[Settings, Depends(get_settings)]
FileDep = Annotated[UploadFile, File(description="PDF document to upload.")]


def _remove_partial_file(path: Path) -> None:
    """Delete a partially written file, ignoring if it is already gone."""
    path.unlink(missing_ok=True)


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(file: FileDep, settings: SettingsDep) -> UploadResponse:
    """Accept and store a single PDF document.

    Rejects non-PDF, empty, and oversized uploads. On success, stores the file
    under a generated internal name and returns its metadata.
    """
    original_filename = sanitize_filename(file.filename or "")
    if not original_filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files (.pdf) are accepted.",
        )

    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    document_id = uuid4().hex
    stored_filename = f"{document_id}.pdf"
    destination = upload_dir / stored_filename

    try:
        size_bytes = await stream_upload_to_path(
            file, destination, settings.max_upload_size_bytes
        )
    except (InvalidPDFError, EmptyUploadError) as exc:
        _remove_partial_file(destination)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except FileTooLargeError as exc:
        _remove_partial_file(destination)
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail=str(exc),
        ) from exc

    return UploadResponse(
        document_id=document_id,
        filename=original_filename,
        stored_filename=stored_filename,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=size_bytes,
    )
