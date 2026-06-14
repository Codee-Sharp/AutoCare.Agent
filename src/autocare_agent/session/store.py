import hashlib
from uuid import UUID

from redis.asyncio import Redis

from autocare_agent.domain.models import SessionContext


def session_key(session_id: UUID) -> str:
    return f"autocare:session:{hashlib.sha256(str(session_id).encode()).hexdigest()}"


class InMemorySessionStore:
    def __init__(self) -> None:
        self.data: dict[str, SessionContext] = {}

    async def get(self, session_id: UUID) -> SessionContext | None:
        return self.data.get(session_key(session_id))

    async def set(self, session_id: UUID, context: SessionContext) -> None:
        self.data[session_key(session_id)] = context

    async def ping(self) -> bool:
        return True


class RedisSessionStore:
    def __init__(self, redis: Redis, ttl_seconds: int) -> None:
        self.redis = redis
        self.ttl_seconds = ttl_seconds

    async def get(self, session_id: UUID) -> SessionContext | None:
        raw = await self.redis.get(session_key(session_id))
        return SessionContext.model_validate_json(raw) if raw else None

    async def set(self, session_id: UUID, context: SessionContext) -> None:
        await self.redis.set(session_key(session_id), context.model_dump_json(), ex=self.ttl_seconds)

    async def ping(self) -> bool:
        return bool(await self.redis.ping())
