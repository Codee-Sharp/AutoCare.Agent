from functools import lru_cache

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables or a local .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    app_auth_token: SecretStr = SecretStr("local-development-token")
    composer_base_url: str = "https://api-for-cursor.standardagents.ai/opencode/v1"
    composer_api_key: SecretStr = SecretStr("")
    composer_model: str = "composer-2.5"
    composer_timeout_seconds: float = Field(default=10, gt=0)
    max_message_length: int = Field(default=4000, ge=1, le=20000)
    log_level: str = "INFO"
    crisis_guidance_code: str = "contact_emergency_services"

    @model_validator(mode="after")
    def validate_composer_configuration(self) -> "Settings":
        if not self.composer_api_key.get_secret_value():
            raise ValueError("COMPOSER_API_KEY is required")
        if not self.composer_base_url.startswith("https://"):
            raise ValueError("COMPOSER_BASE_URL must use HTTPS")
        if not self.composer_model.strip():
            raise ValueError("COMPOSER_MODEL cannot be blank")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
