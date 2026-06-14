# Implementation Plan: Fundação Simplificada do Serviço de Agente

**Branch**: `001-agent-service-foundation` | **Date**: 2026-06-14 | **Spec**:
[spec.md](./spec.md)

## Summary

Construir um microserviço stateless que recebe mensagens e contexto mínimo da
aplicação interna, aplica segurança determinística, chama um provider LLM e
retorna resposta e ações estruturadas. A aplicação interna permanece
responsável por estado, persistência, integrações e regras de negócio.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Uvicorn, LangGraph, Pydantic v2,
pydantic-settings e HTTPX assíncrono

**Storage**: nenhum; o contexto necessário é enviado pela aplicação interna em
cada request

**Testing**: pytest, pytest-asyncio e respx; stubs privados da suíte para
execução sem rede

**Target Platform**: contêiner Linux atrás da aplicação interna

**Constraints**: contratos validados, timeouts explícitos, contexto mínimo,
logs sanitizados, nenhuma ação crítica executada pelo Agent e nenhuma
confirmação inventada

## Architecture

```text
src/autocare_agent/
├── app.py
├── config.py
├── schemas.py
├── orchestrator.py
├── llm.py
├── safety.py
├── actions.py
└── logging.py
```

### Decisions

- O `Orchestrator` compila um LangGraph pequeno com estado tipado e nodes
  mantidos juntos enquanto o fluxo for simples.
- O serviço não usa Redis; a aplicação interna já é proprietária do estado.
- O serviço não chama tools REST; a aplicação interna já orquestra dados e
  ações autoritativas.
- `LLMProvider` é a única abstração de infraestrutura necessária.
- Crise, risco ambíguo e pedido humano interrompem o fluxo antes do LLM.
- Falha ou resposta inválida do provider resulta em resposta segura e handoff.
- Ações críticas são apenas propostas estruturadas para execução externa.

## SOLID and KISS

- **SRP**: contratos, segurança, provider, ações, logs e HTTP possuem módulos
  focados.
- **DIP**: `Orchestrator` depende de `LLMProvider`, não de Composer.
- **KISS**: LangGraph é usado sem criar um package e arquivo para cada node;
  não existem stores ou clientes sem uso atual.
- Novas abstrações devem ser adicionadas apenas quando houver complexidade real.

## Request Flow

```text
POST /agent/process
  -> autenticar e propagar request_id
  -> validar e sanitizar input
  -> detectar crise e pedido humano
  -> reconhecer resultado autoritativo
  -> classificar intenção
  -> construir prompt mínimo
  -> chamar LLMProvider
  -> validar ações
  -> responder e registrar evento sanitizado
```

## Verification

- Testar request/response, autenticação, health e Swagger.
- Testar mensagem normal com stub privado da suíte.
- Testar crise, risco ambíguo e pedido humano sem chamar LLM.
- Testar timeout, falha e conteúdo inválido do provider.
- Testar bloqueio de ações críticas inválidas ou com request ID incorreto.
- Testar sanitização de logs e rejeição de contexto inesperado.
- Executar `pytest`, Ruff e mypy sem acesso real à rede.

## Out of Scope

- Persistência e Redis
- Múltiplos agentes e persistência/checkpoints do LangGraph
- Clientes REST para a aplicação interna
- PostgreSQL e pagamentos
- Execução de ações críticas
- Regras definitivas de negócio
- Diagnóstico médico
