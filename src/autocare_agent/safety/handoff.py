HUMAN_TERMS = {"atendente", "humano", "pessoa", "falar com alguém", "falar com alguem"}


def requests_human(message: str) -> bool:
    lowered = message.lower()
    return any(term in lowered for term in HUMAN_TERMS)
