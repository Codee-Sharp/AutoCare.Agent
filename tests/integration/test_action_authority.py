from uuid import uuid4


def test_authoritative_success_requires_protocol(client, auth_headers, process_payload) -> None:
    process_payload["contexto"]["resultado_autoritativo"] = {
        "action_id": str(uuid4()),
        "status": "success",
    }
    assert client.post("/agent/process", headers=auth_headers, json=process_payload).status_code == 422


def test_authoritative_success_with_protocol(client, auth_headers, process_payload) -> None:
    process_payload["contexto"]["resultado_autoritativo"] = {
        "action_id": str(uuid4()),
        "status": "success",
        "protocolo": "AG-123",
    }
    body = client.post("/agent/process", headers=auth_headers, json=process_payload).json()
    assert "AG-123" in body["resposta_texto"]
