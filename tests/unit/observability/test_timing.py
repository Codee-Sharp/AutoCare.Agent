import pytest

from autocare_agent.observability.instrumentation import timed


@pytest.mark.asyncio
async def test_timing_reports_duration() -> None:
    durations: list[float] = []
    async with timed(durations.append):
        pass
    assert len(durations) == 1
    assert durations[0] >= 0
