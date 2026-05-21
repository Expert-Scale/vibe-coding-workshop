import socket
import subprocess
import sys
import time

import httpx
import pytest


def _pick_free_port() -> int:
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture(scope="module")
def server():
    port = _pick_free_port()
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.flag_clauses:app", "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"
    for _ in range(50):
        try:
            httpx.get(f"{base_url}/docs", timeout=0.5)
            break
        except (httpx.RequestError, httpx.HTTPError):
            time.sleep(0.1)
    else:
        proc.terminate()
        pytest.fail("uvicorn did not start in time")
    yield base_url
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def test_endpoint_returns_critical_flag(server):
    r = httpx.post(
        f"{server}/flag-clauses",
        json={"text": "Vendor accepts unlimited liability for all damages."},
    )
    assert r.status_code == 200
    flags = r.json()["flags"]
    assert any(f["rule"] == "unlimited_liability" and f["severity"] == "critical" for f in flags)


def test_endpoint_rejects_missing_text(server):
    r = httpx.post(f"{server}/flag-clauses", json={"wrong_field": "x"})
    assert r.status_code == 422


def test_endpoint_clean_text(server):
    r = httpx.post(f"{server}/flag-clauses", json={"text": "We're shipping widgets next quarter."})
    assert r.status_code == 200
    assert r.json() == {"flags": []}


def test_endpoint_handles_long_realistic_paragraph(server):
    text = (
        "This Master Services Agreement (the 'Agreement') is entered into between the parties. "
        "Vendor agrees to provide services with unlimited liability for any breach. "
        "The term shall be perpetual unless terminated by either party. "
        "Vendor will deposit all source code into source code escrow. "
        "Auto-renewal shall apply on each anniversary."
    )
    r = httpx.post(f"{server}/flag-clauses", json={"text": text})
    assert r.status_code == 200
    rules = {f["rule"] for f in r.json()["flags"]}
    assert {"unlimited_liability", "perpetual_term", "source_code_escrow", "auto_renewal"} <= rules
