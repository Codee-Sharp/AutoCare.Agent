from autocare_agent.config.settings import Settings


def test_settings_hide_secrets() -> None:
    settings = Settings(app_auth_token="super-secret")
    assert "super-secret" not in repr(settings)
    assert settings.session_ttl_seconds == 1800
