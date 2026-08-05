"""Pydantic response models for the API."""

from pydantic import BaseModel, Field


class RootResponse(BaseModel):
    """Basic service information returned by the root endpoint."""

    app_name: str = Field(description="Configured application name.")
    version: str = Field(description="Semantic version of the application.")
    docs_url: str = Field(description="Path to the interactive API docs.")


class HealthResponse(BaseModel):
    """Payload returned by the health-check endpoint."""

    status: str = Field(description="Overall service status.")
    app_name: str = Field(description="Configured application name.")
    environment: str = Field(description="Deployment environment name.")


class VersionResponse(BaseModel):
    """Payload returned by the version endpoint."""

    version: str = Field(description="Semantic version of the application.")
    app_name: str = Field(description="Configured application name.")


class UploadResponse(BaseModel):
    """Metadata returned after a successful document upload."""

    document_id: str = Field(description="Unique identifier for the document.")
    filename: str = Field(description="Sanitized original filename.")
    stored_filename: str = Field(description="Internal filename used on disk.")
    content_type: str = Field(description="Reported MIME type of the upload.")
    size_bytes: int = Field(description="Size of the stored file in bytes.")
