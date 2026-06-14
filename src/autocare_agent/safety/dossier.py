from autocare_agent.domain.models import HandoffDossier, Intent, ProposedAction


def build_dossier(reason: str, intent: Intent, actions: list[ProposedAction] | None = None) -> HandoffDossier:
    allowed = {"pedido_explicito", "falha_segura", "risco_ambiguo", "incapaz_responder"}
    safe_reason = reason if reason in allowed else "incapaz_responder"
    return HandoffDossier(
        motivo=safe_reason,  # type: ignore[arg-type]
        intencao=intent,
        resumo_sanitizado=f"Transferência solicitada. Motivo: {safe_reason}.",
        acoes_pendentes=actions or [],
    )
