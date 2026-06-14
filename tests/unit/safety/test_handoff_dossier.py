from autocare_agent.domain.models import Intent
from autocare_agent.safety.dossier import build_dossier


def test_handoff_dossier_is_minimal() -> None:
    dossier = build_dossier("pedido_explicito", Intent.HUMAN)
    dumped = dossier.model_dump()
    assert dumped["motivo"] == "pedido_explicito"
    assert "mensagem" not in dumped
    assert "paciente_id" not in dumped
