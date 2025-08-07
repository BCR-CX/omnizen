"""
Tests for the Omnizen settings module.
"""

import os
from unittest.mock import patch

from omnizen.settings import Settings, settings


def test_settings_default_values():
    """
    Test that Settings class initializes with correct default values.
    """
    test_settings = Settings()

    assert test_settings.domain == "omnizen"
    assert test_settings.email == "user@example.com"
    assert test_settings.api_token == "your_api_token_here"


def test_settings_uppercase_environment_variables():
    """
    Test that Settings can be initialized from uppercase environment variables.
    """
    env_vars = {
        "ZENDESK_DOMAIN": "test_domain",
        "ZENDESK_EMAIL": "test@example.com",
        "ZENDESK_API_TOKEN": "test_token_123",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        test_settings = Settings()

        assert test_settings.domain == "test_domain"
        assert test_settings.email == "test@example.com"
        assert test_settings.api_token == "test_token_123"


def test_settings_random_case_environment_variables():
    """
    Test that Settings can be initialized from environment variables with random case.
    """
    env_vars = {
        "zendesk_DOMAIN": "test_domain",
        "ZENDESK_email": "test@example.com",
        "zendesk_API_TOKEN": "test_token_123",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        test_settings = Settings()

        assert test_settings.domain == "test_domain"
        assert test_settings.email == "test@example.com"
        assert test_settings.api_token == "test_token_123"


def test_settings_direct_initialization():
    """
    Test that Settings can be initialized with direct parameter values.
    """
    test_settings = Settings(
        domain="custom_domain",
        email="custom@example.com",
        api_token="custom_token_456",
    )

    assert test_settings.domain == "custom_domain"
    assert test_settings.email == "custom@example.com"
    assert test_settings.api_token == "custom_token_456"


def test_settings_from_environment_variables():
    """
    Test that Settings can be initialized from environment variables.
    """
    env_vars = {
        "zendesk_domain": "test_domain",
        "zendesk_email": "test@example.com",
        "zendesk_api_token": "test_token_123",
    }

    with patch.dict(os.environ, env_vars, clear=False):
        test_settings = Settings()

        assert test_settings.domain == "test_domain"
        assert test_settings.email == "test@example.com"
        assert test_settings.api_token == "test_token_123"


def test_global_settings_instance():
    """
    Test that the global settings instance is created and accessible.
    """
    assert settings is not None
    assert isinstance(settings, Settings)
    assert settings.domain == "omnizen"
    assert settings.email == "user@example.com"
    assert settings.api_token == "your_api_token_here"
