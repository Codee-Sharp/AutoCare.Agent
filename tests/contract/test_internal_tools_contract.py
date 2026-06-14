from pathlib import Path

import yaml


def test_internal_tool_contract_is_read_only() -> None:
    contract = yaml.safe_load(
        Path("specs/001-agent-service-foundation/contracts/internal-tools.openapi.yaml").read_text()
    )
    assert contract["x-agent-proposed-actions"] == ["confirmar_agendamento", "cancelar_agendamento"]
    assert all(operation["post"]["x-agent-mode"] == "query" for operation in contract["paths"].values())
