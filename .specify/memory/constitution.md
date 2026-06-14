<!--
Sync Impact Report
- Version change: template -> 1.0.0
- Added principles:
  - I. Safety First and Human Escalation
  - II. Privacy and Minimum Necessary Data
  - III. Deterministic Backend Authority
  - IV. Transactional Integrity
  - V. Observable and Testable Contracts
- Added sections:
  - Architecture and Security Constraints
  - Development Workflow and Quality Gates
- Removed sections: none
- Templates:
  - updated: .specify/templates/plan-template.md
  - updated: .specify/templates/spec-template.md
  - updated: .specify/templates/tasks-template.md
  - pending: .specify/templates/commands/*.md (directory does not exist)
- Runtime guidance:
  - verified: README.md
  - verified: wiki/STACK_REAL.md
  - verified: wiki/ARQUITETURA.md
  - verified: wiki/REGRAS_NEGOCIO.md
- Deferred items: none
-->
# AutoCare Agent Constitution

## Core Principles

### I. Safety First and Human Escalation
Patient safety MUST take priority over conversational fluency, conversion, and
automation. The Agent MUST interrupt the normal flow when it detects a medical
or psychological crisis, return the configured emergency guidance, and trigger
the appropriate human or clinical escalation. The Agent MUST offer human
handoff when it cannot safely resolve a request, when required information is
unavailable, or when a patient requests a person. Safety-critical behavior MUST
have explicit acceptance scenarios and automated tests.

### II. Privacy and Minimum Necessary Data
Only data necessary for the current interaction MAY be sent to the Agent or an
LLM provider. Secrets, payment data, authoritative prices, discount rules, and
unnecessary clinical or personal data MUST NOT enter prompts or model-visible
logs. Sensitive data MUST be protected in transit and at rest, access MUST be
authorized, and critical access or changes MUST be auditable. Logs MUST support
diagnosis without exposing sensitive prompt content or patient identifiers.

### III. Deterministic Backend Authority
The LLM MAY interpret intent, conduct conversations, and propose structured
actions, but it MUST NOT be the authority for business rules, prices,
discounts, payments, availability, or persisted state. All critical facts and
actions MUST be obtained or executed through typed REST tools backed by the
internal application. The Agent MUST NOT access the primary database directly.
When an authoritative tool is unavailable, the Agent MUST fail safely rather
than inventing a result.

### IV. Transactional Integrity
Scheduling, cancellation, payment, discount, and other state-changing
operations MUST be validated and committed by the internal application using
appropriate concurrency control. Critical commands MUST be idempotent or carry
an explicit deduplication strategy. Scheduling MUST prevent double-booking,
define lock expiration behavior, and preserve a recoverable outcome on timeout
or partial failure. The Agent MUST only claim success after receiving an
authoritative confirmation and protocol from the internal application.

### V. Observable and Testable Contracts
Agent requests, tool calls, tool responses, actions, crisis alerts, and handoff
payloads MUST use versioned, validated, structured contracts. Critical flows
MUST emit traceable outcomes and sanitized logs with correlation identifiers.
Every feature MUST include tests proportional to its risk; safety, privacy,
state-changing operations, and external integrations require automated
contract and integration tests. Failure paths, timeouts, malformed responses,
and provider fallback behavior MUST be tested before release.

## Architecture and Security Constraints

- The AutoCare Agent is a Python and LangGraph microservice behind the internal
  application; the internal application owns persistence, payments,
  notifications, and authoritative business validation.
- Redis MAY store short-lived session context, but MUST NOT become the source
  of truth for critical business state.
- All external input and tool output MUST be validated before use.
- Authentication, authorization, rate limiting, encryption, secret management,
  and audit requirements MUST be identified in every affected feature plan.
- Prompt changes, model changes, and fallback-provider changes MUST be treated
  as behavioral changes and validated against safety and regression scenarios.

## Development Workflow and Quality Gates

1. Each feature specification MUST identify safety, privacy, human-handoff,
   authoritative-data, and failure-mode impacts.
2. Each implementation plan MUST pass the Constitution Check before research
   and again after design. Any exception requires documented justification and
   explicit approval.
3. Tasks MUST include contract validation, observability, and automated tests
   for every affected critical path before implementation is considered done.
4. Changes MUST be reviewed for direct database access, sensitive-data
   exposure, invented authoritative facts, unsafe failure behavior, and
   transaction or concurrency regressions.
5. A feature MAY be released only after its acceptance scenarios and required
   automated tests pass.

## Governance

This constitution supersedes conflicting project practices and feature-level
decisions. Amendments require a documented rationale, an impact assessment for
dependent templates and active features, and approval by a project maintainer.
Constitution versions follow semantic versioning: MAJOR for incompatible
principle or governance changes, MINOR for new principles or materially
expanded requirements, and PATCH for clarifications without changed meaning.
Every plan and code review MUST verify compliance; unresolved violations block
implementation or release unless the constitution is amended explicitly.

**Version**: 1.0.0 | **Ratified**: 2026-06-13 | **Last Amended**: 2026-06-13
