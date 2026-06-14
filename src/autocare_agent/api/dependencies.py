from functools import lru_cache

import httpx
from redis.asyncio import Redis

from autocare_agent.config.settings import get_settings
from autocare_agent.domain.protocols import LLMProvider
from autocare_agent.graph.workflow import Workflow, build_workflow
from autocare_agent.llm.providers import ComposerLLMProvider, FakeLLMProvider
from autocare_agent.session.store import InMemorySessionStore, RedisSessionStore

_memory_store = InMemorySessionStore()


@lru_cache
def get_session_store() -> InMemorySessionStore | RedisSessionStore:
    settings = get_settings()
    if settings.app_env in {"production", "staging"}:
        return RedisSessionStore(Redis.from_url(settings.redis_url), settings.session_ttl_seconds)
    return _memory_store


@lru_cache
def get_workflow() -> Workflow:
    settings = get_settings()
    if settings.llm_provider == "composer":
        provider: LLMProvider = ComposerLLMProvider(
            httpx.AsyncClient(),
            settings.composer_base_url,
            settings.composer_api_key.get_secret_value(),
            settings.composer_model,
            settings.composer_timeout_seconds,
        )
    else:
        provider = FakeLLMProvider()
    return build_workflow(
        provider,
        get_session_store(),
        settings.session_ttl_seconds,
        settings.crisis_guidance_code,
    )
