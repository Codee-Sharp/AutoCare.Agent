def test_normal_request(client, auth_headers, process_payload) -> None:
    response = client.post("/agent/process", headers=auth_headers, json=process_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["sucesso"] is True
    assert body["request_id"] == auth_headers["X-Request-ID"]


def test_agent_requires_authentication(client, process_payload) -> None:
    assert client.post("/agent/process", json=process_payload).status_code == 401


def test_invalid_request_is_rejected(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = " "
    assert client.post("/agent/process", headers=auth_headers, json=process_payload).status_code == 422
