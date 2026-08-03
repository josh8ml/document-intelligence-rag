"""Unit tests for application configuration."""

from app.core.config import Settings, get_settings


def test_settings_expose_expected_fields() -> None:
    """Settings expose typed application fields."""
    settings = get_settings()
    assert isinstance(settings.app_name, str)
    assert isinstance(settings.api_port, int)


def test_get_settings_returns_cached_instance() -> None:
    """get_settings returns the same object on repeated calls (cached)."""
    assert get_settings() is get_settings()


def test_settings_declares_defaults() -> None:
    """The Settings class declares the expected default values."""
    fields = Settings.model_fields
    assert fields["app_name"].default == "Document Intelligence RAG Platform"
    assert fields["api_port"].default == 8000
    assert fields["app_env"].default == "development"
