import time
from http import HTTPStatus
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_concurrent_performance_testclient(sign_url):
    payload = {"msg": "concurrent_test_msg"}
    count = 100
    max_workers = 10

    def send_request():
        return client.post(sign_url, json=payload)

    client.post(sign_url, json=payload)

    start_time = time.perf_counter()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(count)]
        responses = [f.result() for f in futures]

    end_time = time.perf_counter()

    for resp in responses:
        assert resp.status_code == HTTPStatus.OK
        assert "signature" in resp.json()

    duration = end_time - start_time
    rps = count / duration

    assert rps >= 100, f"RPS {rps:.2f} ниже требуемого порога 100"
