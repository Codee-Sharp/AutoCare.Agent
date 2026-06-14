def test_explicit_handoff(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = "Quero falar com um atendente humano"
    body = client.post("/agent/process", headers=auth_headers, json=process_payload).json()
    assert body["dossie_handoff"]["motivo"] == "pedido_explicito"
