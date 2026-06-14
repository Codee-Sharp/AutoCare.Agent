import pytest
from pydantic import ValidationError

from autocare_agent.app import get_orchestrator
from autocare_agent.config import Settings
from autocare_agent.llm import ComposerLLMProvider


def test_settings_hide_secrets_and_have_no_storage_configuration() -> None:
    settings = Settings(app_auth_token="super-secret", composer_api_key="test-key")

    assert "super-secret" not in repr(settings)
    assert not hasattr(settings, "redis_url")
    assert not hasattr(settings, "llm_provider")
    assert settings.composer_model == "composer-2.5"
    assert settings.composer_base_url == "https://api-for-cursor.standardagents.ai/opencode/v1"


def test_composer_requires_api_key_and_https() -> None:
    with pytest.raises(ValidationError):
        Settings(composer_api_key="")
    with pytest.raises(ValidationError):
        Settings(composer_api_key="key", composer_base_url="http://composer.test")


def test_runtime_uses_only_composer_provider() -> None:
    assert isinstance(get_orchestrator().provider, ComposerLLMProvider)
    assert get_orchestrator().provider.model == "composer-2.5"
