from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_auth_token: SecretStr = SecretStr("local-development-token")
    llm_provider: Literal["fake", "composer"] = "fake"
    composer_base_url: str = "https://composer.example.invalid/v1"
    composer_api_key: SecretStr = SecretStr("")
    composer_model: str = "composer-2"
    composer_timeout_seconds: float = Field(default=10, gt=0)
    internal_app_base_url: str = "https://internal.example.invalid"
    internal_app_api_key: SecretStr = SecretStr("")
    internal_app_timeout_seconds: float = Field(default=5, gt=0)
    redis_url: str = "redis://localhost:6379/0"
    session_ttl_seconds: int = Field(default=1800, ge=60, le=86400)
    max_message_length: int = Field(default=4000, ge=1, le=20000)
    log_level: str = "INFO"
    crisis_guidance_code: str = "contact_emergency_services"


@lru_cache
def get_settings() -> Settings:
    return Settings()
