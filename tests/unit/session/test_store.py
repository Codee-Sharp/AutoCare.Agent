from uuid import uuid4

import pytest

from autocare_agent.domain.models import SessionContext
from autocare_agent.session.store import InMemorySessionStore


@pytest.mark.asyncio
async def test_memory_session_round_trip() -> None:
    store = InMemorySessionStore()
    session_id = uuid4()
    context = SessionContext(sessao_hash="hash")
    await store.set(session_id, context)
    assert await store.get(session_id) == context
    assert await store.ping()
