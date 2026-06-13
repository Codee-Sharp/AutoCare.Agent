# Implementation Plan: Fundação do Serviço de Agente

**Branch**: `001-agent-service-foundation` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-agent-service-foundation/spec.md`

## Summary

Construir um microserviço assíncrono que recebe mensagens da aplicação interna,
orquestra um fluxo seguro de conversa, consulta fontes autoritativas quando
necessário e retorna respostas e ações propostas em contratos validados. O
domínio permanece isolado de FastAPI, Redis, HTTPX e providers LLM; falhas de
qualquer dependência produzem resposta segura e handoff quando necessário.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Uvicorn, LangGraph, Pydantic v2,
pydantic-settings, HTTPX assíncrono, redis-py assíncrono

**Storage**: Redis somente para contexto temporário de sessão; sem acesso a
PostgreSQL ou persistência crítica

**Testing**: pytest, pytest-asyncio, respx; FakeLLMProvider e Redis substituível
em testes para execução sem rede

**Target Platform**: Contêiner Linux executado atrás da aplicação interna

**Project Type**: Microserviço REST assíncrono

**Performance Goals**: p95 de `POST /agent/process` até 5 segundos com
dependências disponíveis; health checks até 2 segundos

**Constraints**: Mensagem com limite configurável, timeouts explícitos,
contratos validados, logs sanitizados, nenhuma ação mutável executada pelo
agente, nenhuma confirmação sem fonte autoritativa

**Scale/Scope**: Fundação inicial para uma instância ou múltiplas réplicas
stateless compartilhando Redis; meta inicial de 10 requisições por segundo por
réplica sem comprometer limites das dependências

## Constitution Check

*GATE: Passed before research and passed again after Phase 1 design.*

- **Safety and Handoff: PASS**. O detector determinístico de crise executa antes
  do LLM e interrompe o fluxo. Falhas inseguras e pedidos humanos produzem
  handoff. Testes unitários e de integração cobrem ambos.
- **Privacy: PASS**. O LLM recebe somente mensagem sanitizada, intenção e resumo
  mínimo permitido. Logs usam sessão anonimizada e nunca incluem mensagem,
  prompt, token, CPF, pagamento ou conteúdo clínico. Contexto Redis possui TTL
  configurável, padrão de 30 minutos.
- **Backend Authority: PASS**. Consultas usam clientes REST tipados da aplicação
  interna. Ações mutáveis são apenas propostas; o agente não executa
  confirmação/cancelamento nem acessa banco de dados.
- **Transactional Integrity: PASS**. A aplicação interna valida, autoriza,
  deduplica e executa ações mutáveis. Cada proposta inclui `request_id` e
  `action_id`; sucesso só pode ser informado quando vier no contexto
  autoritativo de uma solicitação posterior.
- **Contracts and Observability: PASS**. Contratos versionados e validados
  propagam `request_id`; logs estruturados registram node, duração e resultado
  externo sanitizado. Testes de contrato cobrem APIs expostas e consumidas.

## Design Decisions

- O grafo possui nodes explícitos: validar entrada, recuperar sessão, detectar
  crise, construir prompt mínimo, classificar intenção, processar LLM, validar
  ações, persistir sessão e construir resposta.
- A rota de crise sai diretamente para a resposta final e não chama LLM, tools
  ou persistência de mensagem completa.
- `LLMProvider` é um protocolo de domínio. `ComposerLLMProvider` usa uma API
  compatível com OpenAI por HTTP e `FakeLLMProvider` retorna fixtures
  determinísticas.
- Tools de leitura (`buscar_disponibilidade`, `consultar_servico`,
  `validar_desconto`, `listar_agendamentos`) podem consultar a aplicação
  interna. Tools mutáveis (`confirmar_agendamento`, `cancelar_agendamento`)
  existem como contratos de ação proposta e não são chamadas pelo agente.
- Autenticação de entrada usa bearer token configurável compartilhado com a
  aplicação interna. Health checks permanecem sem autenticação. Rate limiting
  de borda pertence à aplicação interna/proxy.
- Readiness depende de configuração válida e Redis acessível; indisponibilidade
  do LLM ou da aplicação interna degrada solicitações com resposta segura, sem
  tornar a instância não pronta.

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-service-foundation/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── agent-api.openapi.yaml
│   └── internal-tools.openapi.yaml
└── tasks.md
```

### Source Code (repository root)

```text
src/autocare_agent/
├── api/
├── config/
├── domain/
├── graph/
├── llm/
├── tools/
├── safety/
├── session/
└── observability/

tests/
├── unit/
├── integration/
└── contract/
```

**Structure Decision**: Projeto Python único com layout `src`, separando domínio
de adaptadores externos e organizando testes por risco e superfície contratual.

## Delivery Phases

### Phase 1 - Foundation and Contracts

- Criar configuração, modelos de domínio, exceções seguras e contratos.
- Implementar logging sanitizado, autenticação de entrada e health checks.
- Criar abstrações de LLM, sessão e tools com fakes determinísticos.

### Phase 2 - Orchestration and Integrations

- Implementar nodes e roteamento LangGraph.
- Implementar Composer provider, Redis session store e clientes REST de leitura.
- Validar e bloquear ações mutáveis ou inventadas antes da resposta.

### Phase 3 - Verification and Packaging

- Cobrir fluxos normais, crise, handoff e falhas com testes sem rede.
- Adicionar Docker, Compose, `.env.example`, README e exemplos.
- Executar Ruff, mypy e pytest como gates locais.

## Complexity Tracking

Nenhuma violação da constituição identificada.
