from uuid import uuid4

import httpx
import pytest
import respx

from autocare_agent.domain.models import ToolStatus
from autocare_agent.tools.client import RestQueryClient


@pytest.mark.asyncio
@respx.mock
async def test_query_client_propagates_request_id() -> None:
    request_id = uuid4()
    route = respx.post("https://internal.test/tools/consultar-servico").mock(
        return_value=httpx.Response(
            200,
            json={"contract_version": "1.0", "request_id": str(request_id), "status": "success", "data": {}},
        )
    )
    result = await RestQueryClient(httpx.AsyncClient(), "https://internal.test", "key", 1).call(
        "/tools/consultar-servico", uuid4(), {}, request_id
    )
    assert result.status == ToolStatus.SUCCESS
    assert route.calls[0].request.headers["X-Request-ID"] == str(request_id)


@pytest.mark.asyncio
@respx.mock
async def test_query_client_handles_timeout() -> None:
    respx.post("https://internal.test/tools/consultar-servico").mock(side_effect=httpx.ReadTimeout("timeout"))
    result = await RestQueryClient(httpx.AsyncClient(), "https://internal.test", "key", 1).call(
        "/tools/consultar-servico", uuid4(), {}, uuid4()
    )
    assert result.status == ToolStatus.TIMEOUT
