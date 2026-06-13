# Tasks: Fundação do Serviço de Agente

**Input**: Design documents from `specs/001-agent-service-foundation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/,
quickstart.md

**Tests**: Tests are required because the feature specification and constitution
require automated coverage for safety, privacy, contracts, external
integrations, failure paths, timeouts, invalid responses, and offline execution.

**Organization**: Tasks are grouped by user story so each story can be
implemented and verified independently after the shared foundation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it targets different files and has no
  dependency on another incomplete task in the same phase.
- **[Story]**: Maps the task to a user story from spec.md.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize the Python service, tooling, packaging, and local
runtime structure.

- [ ] T001 Create package and test directory structure with `__init__.py` files under `src/autocare_agent/`, `tests/unit/`, `tests/integration/`, and `tests/contract/`
- [ ] T002 Configure Python 3.12 dependencies, pytest, pytest-asyncio, Ruff, and mypy in `pyproject.toml`
- [ ] T003 [P] Add secret-free environment variable template in `.env.example`
- [ ] T004 [P] Add application container build in `Dockerfile`
- [ ] T005 [P] Add application and Redis local services in `docker-compose.yml`
- [ ] T006 [P] Add test fixtures and network-blocking defaults in `tests/conftest.py`

**Checkpoint**: The repository has an installable project skeleton and isolated
test harness.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement contracts and adapters required by every user story.

**CRITICAL**: No user story implementation starts before this phase completes.

### Foundational Tests

- [ ] T007 [P] Add settings validation and secret-redaction unit tests in `tests/unit/config/test_settings.py`
- [ ] T008 [P] Add domain contract validation and forbidden-field tests in `tests/unit/domain/test_models.py`
- [ ] T009 [P] Add sanitized structured logging tests in `tests/unit/observability/test_logging.py`
- [ ] T010 [P] Add fake and Composer LLM provider contract tests, including timeout and invalid content, in `tests/unit/llm/test_providers.py`
- [ ] T011 [P] Add session store contract tests for TTL, invalid context, and unavailable storage in `tests/unit/session/test_store.py`
- [ ] T012 [P] Add exposed API OpenAPI contract validation tests in `tests/contract/test_agent_api_contract.py`
- [ ] T013 [P] Add consumed internal tool OpenAPI contract validation tests in `tests/contract/test_internal_tools_contract.py`

### Foundational Implementation

- [ ] T014 Implement environment settings and provider selection in `src/autocare_agent/config/settings.py`
- [ ] T015 [P] Implement strict request, response, action, crisis, handoff, and tool-result models in `src/autocare_agent/domain/models.py`
- [ ] T016 [P] Implement domain protocols for LLM, session storage, and query tools in `src/autocare_agent/domain/protocols.py`
- [ ] T017 [P] Implement safe domain error types and public error mapping in `src/autocare_agent/domain/errors.py`
- [ ] T018 [P] Implement allowlist-based JSON logging, session anonymization, and timing helpers in `src/autocare_agent/observability/logging.py`
- [ ] T019 Implement deterministic `FakeLLMProvider` and OpenAI-compatible `ComposerLLMProvider` in `src/autocare_agent/llm/providers.py`
- [ ] T020 Implement in-memory and Redis session stores with configurable TTL in `src/autocare_agent/session/store.py`
- [ ] T021 Implement FastAPI dependency wiring for settings, providers, stores, and shared HTTPX client in `src/autocare_agent/api/dependencies.py`
- [ ] T022 Implement bearer-token authentication and request ID propagation middleware in `src/autocare_agent/api/middleware.py`
- [ ] T023 Create FastAPI application factory and router registration in `src/autocare_agent/api/app.py`

**Checkpoint**: Shared contracts, privacy controls, dependencies, and test
doubles are ready.

---

## Phase 3: User Story 1 - Conversa segura e útil (Priority: P1) MVP

**Goal**: Process a normal administrative message with safe context continuity,
intent classification, and a validated response.

**Independent Test**: Send a normal message using `FakeLLMProvider` and verify a
tracked response with intent and validated actions, without external network.

### Tests for User Story 1

- [ ] T024 [P] [US1] Add request and response endpoint tests for normal messages and validation failures in `tests/integration/test_agent_process.py`
- [ ] T025 [P] [US1] Add graph tests for node order, session continuity, LLM timeout, and invalid LLM response in `tests/unit/graph/test_normal_flow.py`
- [ ] T026 [P] [US1] Add prompt minimization and forbidden-data exclusion tests in `tests/unit/llm/test_prompt_builder.py`

### Implementation for User Story 1

- [ ] T027 [P] [US1] Implement input validation and sanitization node in `src/autocare_agent/graph/nodes/input_validation.py`
- [ ] T028 [P] [US1] Implement temporary session load and save nodes in `src/autocare_agent/graph/nodes/session_context.py`
- [ ] T029 [P] [US1] Implement minimal safe prompt builder in `src/autocare_agent/llm/prompt_builder.py`
- [ ] T030 [P] [US1] Implement intent classification node and known intent taxonomy in `src/autocare_agent/graph/nodes/intent.py`
- [ ] T031 [P] [US1] Implement LLM conversation and safe-failure node in `src/autocare_agent/graph/nodes/conversation.py`
- [ ] T032 [US1] Implement typed LangGraph state and normal-flow graph assembly in `src/autocare_agent/graph/workflow.py`
- [ ] T033 [US1] Implement final response construction node in `src/autocare_agent/graph/nodes/response.py`
- [ ] T034 [US1] Implement `POST /agent/process` using the compiled graph in `src/autocare_agent/api/routes/agent.py`

**Checkpoint**: A normal conversation is independently functional and testable
with no real network.

---

## Phase 4: User Story 2 - Interrupção por crise (Priority: P1)

**Goal**: Detect crisis signals before normal processing, interrupt the graph,
and return a structured alert with human escalation.

**Independent Test**: Send a crisis fixture and verify that LLM, query tools, and
normal flow are not called and a sanitized crisis alert is returned.

### Tests for User Story 2

- [ ] T035 [P] [US2] Add deterministic crisis detector tests including ambiguous and non-crisis messages in `tests/unit/safety/test_crisis_detector.py`
- [ ] T036 [P] [US2] Add crisis short-circuit integration tests proving no LLM or tool calls occur in `tests/integration/test_crisis_flow.py`
- [ ] T037 [P] [US2] Add crisis payload privacy and contract tests in `tests/contract/test_crisis_contract.py`

### Implementation for User Story 2

- [ ] T038 [P] [US2] Implement deterministic crisis categories and detector in `src/autocare_agent/safety/crisis.py`
- [ ] T039 [P] [US2] Implement configured non-diagnostic emergency guidance builder in `src/autocare_agent/safety/guidance.py`
- [ ] T040 [US2] Implement crisis detection and alert nodes in `src/autocare_agent/graph/nodes/crisis.py`
- [ ] T041 [US2] Add immediate crisis routing before prompt and LLM nodes in `src/autocare_agent/graph/workflow.py`

**Checkpoint**: Crisis processing is independently verifiable and always takes
priority over normal conversation.

---

## Phase 5: User Story 3 - Solicitação de atendimento humano (Priority: P2)

**Goal**: Produce a minimal, sanitized handoff dossier for explicit requests or
unsafe failure conditions.

**Independent Test**: Send an explicit human-service request and force a
dependency failure; verify both return a sanitized structured handoff.

### Tests for User Story 3

- [ ] T042 [P] [US3] Add explicit human-request detection tests in `tests/unit/safety/test_handoff.py`
- [ ] T043 [P] [US3] Add handoff dossier minimization and forbidden-data tests in `tests/unit/safety/test_handoff_dossier.py`
- [ ] T044 [P] [US3] Add explicit-request and unsafe-failure handoff integration tests in `tests/integration/test_handoff_flow.py`

### Implementation for User Story 3

- [ ] T045 [P] [US3] Implement explicit human-request detector and handoff reason taxonomy in `src/autocare_agent/safety/handoff.py`
- [ ] T046 [P] [US3] Implement sanitized handoff dossier builder in `src/autocare_agent/safety/dossier.py`
- [ ] T047 [US3] Implement handoff graph node and route explicit requests and unsafe failures in `src/autocare_agent/graph/nodes/handoff.py`
- [ ] T048 [US3] Integrate handoff results into final responses in `src/autocare_agent/graph/nodes/response.py`

**Checkpoint**: Handoff behavior works independently for patient requests and
safe degradation.

---

## Phase 6: User Story 4 - Execução por aplicação interna (Priority: P2)

**Goal**: Query authoritative internal APIs through typed clients while
returning state-changing operations only as validated proposals.

**Independent Test**: Exercise all six action types with mocked REST responses;
verify query failures fail safely and confirm/cancel are never called by the
agent.

### Tests for User Story 4

- [ ] T049 [P] [US4] Add REST query client success, timeout, unavailable, invalid response, and request ID propagation tests with respx in `tests/unit/tools/test_clients.py`
- [ ] T050 [P] [US4] Add structured action validation tests including invented and malformed critical actions in `tests/unit/tools/test_action_validator.py`
- [ ] T051 [P] [US4] Add integration tests proving confirm and cancel are proposals and never outbound calls in `tests/integration/test_action_authority.py`
- [ ] T052 [P] [US4] Add authoritative result and protocol response contract tests in `tests/contract/test_authoritative_result_contract.py`

### Implementation for User Story 4

- [ ] T053 [P] [US4] Implement typed request and response contracts for all six tools in `src/autocare_agent/tools/contracts.py`
- [ ] T054 [P] [US4] Implement shared HTTPX REST query client with timeout, validation, and correlation propagation in `src/autocare_agent/tools/client.py`
- [ ] T055 [US4] Implement read-only clients for availability, service, discount, and appointment listing in `src/autocare_agent/tools/queries.py`
- [ ] T056 [P] [US4] Implement critical action proposal factories for confirmation and cancellation in `src/autocare_agent/tools/proposals.py`
- [ ] T057 [US4] Implement action allowlist, parameter validation, mode enforcement, and invented-action blocking in `src/autocare_agent/tools/validator.py`
- [ ] T058 [US4] Implement action validation and authoritative query graph node in `src/autocare_agent/graph/nodes/actions.py`
- [ ] T059 [US4] Integrate query results and proposed actions into normal graph routing in `src/autocare_agent/graph/workflow.py`

**Checkpoint**: The internal application remains the sole authority and executor
for critical actions.

---

## Phase 7: User Story 5 - Operação observável e verificável (Priority: P3)

**Goal**: Expose accurate health checks and trace every flow using sanitized
structured logs.

**Independent Test**: Query live/ready with healthy and unavailable Redis, then
inspect logs from normal, crisis, handoff, and tool-failure flows for required
fields and absence of sensitive data.

### Tests for User Story 5

- [ ] T060 [P] [US5] Add liveness and readiness endpoint tests with healthy and unavailable Redis in `tests/integration/test_health.py`
- [ ] T061 [P] [US5] Add end-to-end structured logging tests for normal, crisis, handoff, and external failure flows in `tests/integration/test_observability.py`
- [ ] T062 [P] [US5] Add operation duration and external-result logging unit tests in `tests/unit/observability/test_timing.py`

### Implementation for User Story 5

- [ ] T063 [P] [US5] Implement liveness and Redis-backed readiness routes in `src/autocare_agent/api/routes/health.py`
- [ ] T064 [P] [US5] Implement node timing and external-call result instrumentation in `src/autocare_agent/observability/instrumentation.py`
- [ ] T065 [US5] Integrate sanitized node, intent, duration, external result, crisis, and handoff logs across `src/autocare_agent/graph/workflow.py`

**Checkpoint**: Operators can verify readiness and diagnose flows without
exposing sensitive content.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Complete packaging, documentation, regression verification, and
quality gates across all stories.

- [ ] T066 [P] Document architecture, safety boundaries, environment variables, commands, and request example in `README.md`
- [ ] T067 [P] Document architectural decisions and rejected alternatives in `docs/architecture-decisions.md`
- [ ] T068 [P] Add full offline regression tests for duplicate requests and concurrent same-session requests in `tests/integration/test_resilience.py`
- [ ] T069 [P] Add performance acceptance tests for process and health latency targets in `tests/integration/test_performance.py`
- [ ] T070 Validate Docker Compose startup and every command from `specs/001-agent-service-foundation/quickstart.md`
- [ ] T071 Run and fix Ruff checks and formatting across `src/` and `tests/`
- [ ] T072 Run and fix mypy checks across `src/`
- [ ] T073 Run and fix the full pytest suite and confirm no test uses real network access in `tests/`
- [ ] T074 Review all source and tests for direct database access, sensitive-data exposure, invented authoritative facts, and unsafe failure behavior in `src/` and `tests/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies.
- **Phase 2 Foundational**: Depends on Phase 1 and blocks all user stories.
- **US1 and US2 (P1)**: Start after Phase 2 and can proceed in parallel.
- **US3 (P2)**: Starts after Phase 2; integration task T048 uses the response
  node introduced by US1.
- **US4 (P2)**: Starts after Phase 2; graph integration tasks T058-T059 use the
  workflow introduced by US1.
- **US5 (P3)**: Starts after Phase 2; end-to-end observability integration T065
  follows desired story flows.
- **Phase 8 Polish**: Depends on all stories selected for release.

### User Story Dependency Graph

```text
Setup -> Foundational -> US1
                    ├-> US2
                    ├-> US3 -> integrate with US1 response
                    ├-> US4 -> integrate with US1 workflow
                    └-> US5 -> observe completed flows
```

### Within Each User Story

- Write tests first and confirm they fail for the intended reason.
- Implement contracts/models before services and nodes.
- Implement services/nodes before routing or endpoint integration.
- Complete the independent test before moving to the next story.

## Parallel Opportunities

- Setup tasks T003-T006 can run in parallel after T001/T002 decisions are known.
- Foundational tests T007-T013 can run in parallel.
- Foundational implementations T015-T018 can run in parallel after settings
  conventions are established.
- US1 node implementations T027-T031 can run in parallel after their tests.
- US2 tests T035-T037 and implementations T038-T039 can run in parallel.
- US3 tests T042-T044 and implementations T045-T046 can run in parallel.
- US4 tests T049-T052 and implementations T053-T054/T056 can run in parallel.
- US5 tests T060-T062 and implementations T063-T064 can run in parallel.
- Documentation, resilience, and performance tasks T066-T069 can run in
  parallel after story completion.

## Parallel Example: User Story 4

```text
Task T049: REST client failure and correlation tests
Task T050: Structured action validation tests
Task T051: Critical actions never invoked integration test
Task T052: Authoritative result contract tests

Then in parallel:
Task T053: Tool contracts
Task T054: Shared REST query client
Task T056: Critical action proposal factories
```

## Implementation Strategy

### MVP First

1. Complete Setup and Foundational phases.
2. Complete US1 for deterministic normal conversation.
3. Complete US2 before exposing the MVP because crisis interruption is a
   mandatory safety gate.
4. Validate US1 and US2 independently with no real network.

### Incremental Delivery

1. Foundation + US1 + US2: safe conversational MVP.
2. Add US3: explicit and failure-driven human handoff.
3. Add US4: authoritative queries and validated critical proposals.
4. Add US5: operational readiness and end-to-end sanitized observability.
5. Complete cross-cutting packaging and quality gates.

## Notes

- `[P]` tasks target separate files or independent tests.
- Story labels provide traceability to spec.md.
- The agent never executes confirmation or cancellation.
- No task may introduce direct PostgreSQL access or real payment processing.
- Every external call must carry an explicit timeout and `request_id`.
- Tests must not access the real network.
