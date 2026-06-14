from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from time import perf_counter


@asynccontextmanager
async def timed(callback: Callable[[float], None]) -> AsyncIterator[None]:
    started = perf_counter()
    try:
        yield
    finally:
        callback(round((perf_counter() - started) * 1000, 2))
