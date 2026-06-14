# Architecture Decisions

## Agent Authority

The Agent may query authoritative internal APIs, but it never executes
confirmation or cancellation. Those operations are returned as validated
proposals carrying `action_id` and `request_id`.

The Agent reports a critical operation as successful only after a later request
contains a correlated authoritative result with status `success` and a valid
protocol.

## Safety Routing

Deterministic crisis detection runs before prompts, LLM calls, and tools.
Unambiguous crisis signals immediately return configured emergency guidance and
human escalation. Ambiguous risk stops administrative processing and asks one
short confirmation question.

## Privacy

Models reject unexpected context fields. Prompts use only an allowlisted,
minimal context. Logs are built from an allowlist and never receive full
messages, prompts, tokens, CPF, payment data, or clinical content.

Redis stores only a short sanitized summary under a hashed session key with a
configurable TTL. It is not a source of truth.

## Transport, Secrets, and Audit

Production deployments must terminate TLS at the internal gateway and use TLS
for Composer, internal APIs, and Redis. Credentials are supplied only through a
managed secret store exposed as environment variables; `.env` is local-only.

Structured events containing request ID, anonymized session, node, intent,
duration, external result, and coded handoff/crisis reason form the operational
audit trail. Critical business-change auditing remains owned by the internal
application.

## Rejected Alternatives

- Direct PostgreSQL access: violates ownership and privacy boundaries.
- LLM-driven crisis handling only: unsafe during provider failure.
- Agent-executed state changes: expands transactional and authorization risk.
- Free-form tool payloads at domain boundaries: permits invented actions.

