from time import perf_counter


def test_health_and_fake_processing_meet_local_latency_targets(client, auth_headers, process_payload) -> None:
    started = perf_counter()
    assert client.get("/health/live").status_code == 200
    assert perf_counter() - started < 2

    started = perf_counter()
    assert client.post("/agent/process", headers=auth_headers, json=process_payload).status_code == 200
    assert perf_counter() - started < 5
