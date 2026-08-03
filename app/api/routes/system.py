"""System endpoints: root, health check, and version.

These carry no business logic. They exist to confirm the service is running
and to expose basic metadata for humans, load balancers, and deploy tooling.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app import __version__
from app.core.config import Settings, get_settings
from app.models.schemas import HealthResponse, RootResponse, VersionResponse

router = APIRouter(tags=["system"])

# Reusable typed dependency: injects the cached Settings instance.
SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.get("/", response_model=RootResponse)
def root(settings: SettingsDep) -> RootResponse:
    """Return basic service information and a pointer to the API docs."""
    return RootResponse(
        app_name=settings.app_name,
        version=__version__,
        docs_url="/docs",
    )


@router.get("/health", response_model=HealthResponse)
def health(settings: SettingsDep) -> HealthResponse:
    """Report that the service is running."""
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.app_env,
    )


@router.get("/version", response_model=VersionResponse)
def version(settings: SettingsDep) -> VersionResponse:
    """Return the application version."""
    return VersionResponse(version=__version__, app_name=settings.app_name)
