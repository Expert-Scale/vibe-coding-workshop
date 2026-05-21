from fastapi.testclient import TestClient

from app.flag_clauses import MAX_TEXT_LEN, app

client = TestClient(app)


def test_no_flags_for_clean_text():
    r = client.post("/flag-clauses", json={"text": "This is a normal sentence about widgets."})
    assert r.status_code == 200
    assert r.json() == {"flags": []}


def test_flags_unlimited_liability():
    r = client.post("/flag-clauses", json={"text": "Vendor accepts unlimited liability."})
    assert r.status_code == 200
    flags = r.json()["flags"]
    assert any(f["rule"] == "unlimited_liability" for f in flags)
    assert flags[0]["severity"] == "critical"


def test_case_insensitive():
    r = client.post("/flag-clauses", json={"text": "UNLIMITED LIABILITY clause."})
    flags = r.json()["flags"]
    assert any(f["rule"] == "unlimited_liability" for f in flags)


def test_multiple_flags_in_one_text():
    text = (
        "Vendor accepts unlimited liability and we agree to source code escrow. "
        "Term is perpetual."
    )
    r = client.post("/flag-clauses", json={"text": text})
    rules = {f["rule"] for f in r.json()["flags"]}
    assert "unlimited_liability" in rules
    assert "source_code_escrow" in rules
    assert "perpetual_term" in rules


def test_empty_text_returns_no_flags():
    r = client.post("/flag-clauses", json={"text": ""})
    assert r.status_code == 200
    assert r.json() == {"flags": []}


def test_whitespace_only_returns_no_flags():
    r = client.post("/flag-clauses", json={"text": "   \n\t  "})
    assert r.status_code == 200
    assert r.json() == {"flags": []}


def test_missing_text_field_returns_422():
    r = client.post("/flag-clauses", json={"wrong_field": "x"})
    assert r.status_code == 422


def test_oversized_text_returns_400():
    r = client.post("/flag-clauses", json={"text": "x" * (MAX_TEXT_LEN + 1)})
    assert r.status_code == 400


def test_exact_max_length_is_allowed():
    r = client.post("/flag-clauses", json={"text": "x" * MAX_TEXT_LEN})
    assert r.status_code == 200


def test_severity_values_are_known():
    text = (
        "unlimited liability, source code escrow, non-solicitation, "
        "auto-renewal, liquidated damages."
    )
    r = client.post("/flag-clauses", json={"text": text})
    for f in r.json()["flags"]:
        assert f["severity"] in {"info", "warning", "critical"}


def test_match_field_contains_actual_substring():
    r = client.post("/flag-clauses", json={"text": "We agree to unlimited liability."})
    flags = r.json()["flags"]
    assert flags
    assert "unlimited liability" in flags[0]["match"].lower()


def test_unicode_text_does_not_crash():
    r = client.post("/flag-clauses", json={"text": "Café — agreement includes perpetual term 你好."})
    assert r.status_code == 200
    rules = {f["rule"] for f in r.json()["flags"]}
    assert "perpetual_term" in rules
