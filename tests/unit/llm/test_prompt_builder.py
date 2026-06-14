from autocare_agent.domain.models import ConversationContext, Intent
from autocare_agent.llm.prompt_builder import build_system_prompt


def test_prompt_contains_only_allowed_context() -> None:
    prompt = build_system_prompt(ConversationContext(locale="pt-BR", resumo_sessao="resumo"), Intent.GENERAL)
    assert "pt-BR" in prompt
    assert "resumo" in prompt
    assert "CPF" not in prompt
