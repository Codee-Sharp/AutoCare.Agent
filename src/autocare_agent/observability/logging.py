import hashlib
import json
import logging
from typing import Any
from uuid import UUID

ALLOWED_FIELDS = {
    "request_id",
    "session_hash",
    "node",
    "intent",
    "duration_ms",
    "external_result",
    "handoff_reason",
    "crisis_reason",
}


def anonymize_session(session_id: UUID, salt: str = "autocare") -> str:
    return hashlib.sha256(f"{salt}:{session_id}".encode()).hexdigest()[:16]


def safe_event(**fields: Any) -> dict[str, Any]:
    return {key: value for key, value in fields.items() if key in ALLOWED_FIELDS and value is not None}


def log_event(logger: logging.Logger, **fields: Any) -> None:
    logger.info(json.dumps(safe_event(**fields), default=str, sort_keys=True))
