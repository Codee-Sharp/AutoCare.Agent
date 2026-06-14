from uuid import uuid4

from autocare_agent.domain.models import AuthoritativeResult


def test_valid_authoritative_result() -> None:
    result = AuthoritativeResult(action_id=uuid4(), status="success", protocolo="AG-123")
    assert result.protocolo == "AG-123"
