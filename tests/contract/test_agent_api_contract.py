from pathlib import Path

import yaml


def test_agent_openapi_contract_parses() -> None:
    contract = yaml.safe_load(Path("specs/001-agent-service-foundation/contracts/agent-api.openapi.yaml").read_text())
    assert "/agent/process" in contract["paths"]
    assert "/health/ready" in contract["paths"]
