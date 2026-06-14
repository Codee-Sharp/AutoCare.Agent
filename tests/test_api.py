from uuid import uuid4


def test_normal_request(client, auth_headers, process_payload) -> None:
    response = client.post("/agent/process", headers=auth_headers, json=process_payload)

    assert response.status_code == 200
    assert response.json()["sucesso"] is True
    assert response.json()["request_id"] == auth_headers["X-Request-ID"]
    assert response.headers["X-Request-ID"] == auth_headers["X-Request-ID"]


def test_agent_requires_authentication(client, process_payload) -> None:
    response = client.post("/agent/process", json=process_payload)

    assert response.status_code == 401
    assert response.headers["X-Request-ID"]


def test_invalid_request_is_rejected(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = " "

    assert client.post("/agent/process", headers=auth_headers, json=process_payload).status_code == 422


def test_configured_message_limit_is_enforced(client, auth_headers, process_payload) -> None:
    process_payload["mensagem"] = "a" * 4001

    response = client.post("/agent/process", headers=auth_headers, json=process_payload)

    assert response.status_code == 422
    assert response.json() == {"detail": "mensagem exceeds configured maximum"}


def test_authoritative_success_requires_protocol(client, auth_headers, process_payload) -> None:
    process_payload["contexto"]["resultado_autoritativo"] = {
        "action_id": str(uuid4()),
        "status": "success",
    }

    assert client.post("/agent/process", headers=auth_headers, json=process_payload).status_code == 422


def test_authoritative_success_is_reported_without_calling_llm(client, auth_headers, process_payload) -> None:
    process_payload["contexto"]["resultado_autoritativo"] = {
        "action_id": str(uuid4()),
        "status": "success",
        "protocolo": "AG-123",
    }

    body = client.post("/agent/process", headers=auth_headers, json=process_payload).json()

    assert body["sucesso"] is True
    assert "AG-123" in body["resposta_texto"]


def test_health_checks_and_swagger_are_public(client) -> None:
    assert client.get("/health/live").json() == {"status": "live"}
    assert client.get("/health/ready").json() == {"status": "ready"}
    assert client.get("/docs").status_code == 200
    openapi = client.get("/openapi.json").json()
    assert "/agent/process" in openapi["paths"]
    assert openapi["components"]["securitySchemes"]["BearerAuth"] == {
        "type": "http",
        "description": (
            "Informe somente o token configurado em APP_AUTH_TOKEN. O Swagger adicionará o prefixo Bearer."
        ),
        "scheme": "bearer",
    }
    assert openapi["paths"]["/agent/process"]["post"]["security"] == [{"BearerAuth": []}]
    assert "security" not in openapi["paths"]["/health/live"]["get"]


def test_swagger_persists_authorization_during_browser_session(client) -> None:
    docs = client.get("/docs").text

    assert '"persistAuthorization": true' in docs
