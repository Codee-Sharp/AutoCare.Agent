def emergency_guidance(code: str) -> str:
    return (
        "Sua segurança é prioridade. Procure imediatamente os serviços de emergência "
        f"da sua região e aguarde atendimento humano. Referência: {code}."
    )


def confirmation_question() -> str:
    return "Você está em risco imediato ou pensando em se machucar agora?"
