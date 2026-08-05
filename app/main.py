"""FastAPI application entry point.

Run locally with::

    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""

from fastapi import FastAPI

from app import __version__
from app.api.routes import documents, system
from app.core.config import get_settings


def create_app() -> FastAPI:
    """Build and configure the FastAPI application instance."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="Document question-answering platform powered by RAG.",
    )
    application.include_router(system.router)
    application.include_router(documents.router)
    return application


app = create_app()
