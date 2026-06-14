def test_crisis_interrupts_normal_flow(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = "Estou pensando em suicídio"
    body = client.post("/agent/process", headers=auth_headers, json=process_payload).json()
    assert body["sucesso"] is False
    assert body["alerta_crise"]["escalonamento_humano"] is True
    assert body["acoes_requeridas"] == []


def test_ambiguous_risk_asks_one_confirmation(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = "Não aguento mais"
    body = client.post("/agent/process", headers=auth_headers, json=process_payload).json()
    assert "risco imediato" in body["resposta_texto"]
    assert body["acoes_requeridas"] == []
