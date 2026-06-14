import asyncio


def test_duplicate_requests_remain_independent(client, auth_headers, process_payload) -> None:
    first = client.post("/agent/process", headers=auth_headers, json=process_payload)
    second = client.post("/agent/process", headers=auth_headers, json=process_payload)
    assert first.status_code == second.status_code == 200
    assert first.json()["acoes_requeridas"] == second.json()["acoes_requeridas"]


def test_concurrent_session_requests_are_safe(client, auth_headers, process_payload) -> None:
    async def run() -> list[int]:
        return await asyncio.gather(
            *[
                asyncio.to_thread(
                    lambda: client.post("/agent/process", headers=auth_headers, json=process_payload).status_code
                )
                for _ in range(3)
            ]
        )

    assert asyncio.run(run()) == [200, 200, 200]
