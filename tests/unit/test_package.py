"""Verify that the project is installed correctly and importable.

These tests are deliberately trivial. Their job is to fail loudly when the
editable install is missing or stale, which would otherwise surface as
confusing ``ModuleNotFoundError`` failures in every later test module.
"""

from importlib.metadata import version

import app

DISTRIBUTION_NAME = "document-intelligence-rag"


def test_package_is_importable() -> None:
    """The ``app`` package can be imported from an installed environment."""
    assert app.__name__ == "app"


def test_package_declares_a_semantic_version() -> None:
    """``app.__version__`` is a dotted MAJOR.MINOR.PATCH string."""
    assert isinstance(app.__version__, str)

    parts = app.__version__.split(".")
    assert len(parts) == 3, f"Expected MAJOR.MINOR.PATCH, got {app.__version__!r}"
    assert all(part.isdigit() for part in parts)


def test_installed_metadata_matches_package_version() -> None:
    """Packaging metadata and the runtime attribute stay in sync.

    If this fails after a version bump, reinstall with ``pip install -e .``.
    """
    assert version(DISTRIBUTION_NAME) == app.__version__