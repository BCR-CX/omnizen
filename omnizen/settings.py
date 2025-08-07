"""
Settings module for Omnizen application.
This module uses Pydantic for settings management and allows configuration
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or defaults.
    """

    domain: str = "omnizen"
    email: str = "user@example.com"
    api_token: str = "your_api_token_here"

    model_config = SettingsConfigDict(env_prefix="zendesk_")


settings = Settings()
