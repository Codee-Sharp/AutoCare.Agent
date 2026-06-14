from autocare_agent.safety.handoff import requests_human


def test_explicit_human_request() -> None:
    assert requests_human("Quero falar com um atendente")
    assert not requests_human("Quero horários")
