"""Verify that development tooling is configured in ``pyproject.toml``.

This is a smoke test, not a behavioral one. It guards against a config
section being accidentally deleted, which would silently disable linting or
type checking for the whole project. It reads the file directly rather than
importing anything, so it stays fast and dependency-free.
"""

import tomllib
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _load_pyproject() -> dict:
    """Parse pyproject.toml from the repository root."""
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def test_pyproject_exists() -> None:
    """The project metadata file is present at the repo root."""
    assert PYPROJECT.is_file()


def test_ruff_is_configured() -> None:
    """Ruff has a lint rule selection defined."""
    config = _load_pyproject()
    ruff = config["tool"]["ruff"]
    assert ruff["line-length"] == 88
    assert len(ruff["lint"]["select"]) > 0


def test_mypy_is_configured() -> None:
    """mypy is configured to check the app and tests packages."""
    mypy = _load_pyproject()["tool"]["mypy"]
    assert "app" in mypy["files"]
    assert mypy["disallow_untyped_defs"] is True


def test_dev_dependencies_include_quality_tools() -> None:
    """The dev extra pins the tools this milestone relies on."""
    dev_deps = _load_pyproject()["project"]["optional-dependencies"]["dev"]
    joined = " ".join(dev_deps)
    for tool in ("ruff", "mypy", "pre-commit"):
        assert tool in joined
