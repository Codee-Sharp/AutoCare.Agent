from autocare_agent.safety.crisis import detect_crisis


def test_crisis_and_ambiguous_detection() -> None:
    assert detect_crisis("estou pensando em suicídio").level == "crisis"
    assert detect_crisis("não aguento mais").level == "ambiguous"
    assert detect_crisis("quero agendar").level == "none"
