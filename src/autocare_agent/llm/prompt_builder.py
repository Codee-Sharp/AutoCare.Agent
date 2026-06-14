from autocare_agent.domain.models import ConversationContext, Intent

SYSTEM_PROMPT = """You are an administrative conversation assistant.
Never diagnose, invent prices, discounts, availability, or confirmations.
Critical actions must be proposed as structured actions for the internal application.
Return only a JSON object matching the requested contract."""


def build_system_prompt(context: ConversationContext | None, intent: Intent) -> str:
    safe_parts = [SYSTEM_PROMPT, f"intent={intent.value}"]
    if context:
        if context.locale:
            safe_parts.append(f"locale={context.locale}")
        if context.timezone:
            safe_parts.append(f"timezone={context.timezone}")
        if context.resumo_sessao:
            safe_parts.append(f"session_summary={context.resumo_sessao[:500]}")
    return "\n".join(safe_parts)
