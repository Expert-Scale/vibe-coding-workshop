# Clause Flagging Agent — Specification

## Intent
`POST /flag-clauses` takes a contract paragraph and returns a list of flagged clauses with severity (`info` | `warning` | `critical`). Flags come from a static ruleset. Latency target <200ms. JSON in, JSON out. No DB.

## Request

```
POST /flag-clauses
Content-Type: application/json

{
  "text": "string — the contract paragraph to analyze"
}
```

## Response (200)

```json
{
  "flags": [
    {
      "rule": "string — the rule name that matched",
      "severity": "info | warning | critical",
      "match": "string — the exact substring that matched"
    }
  ]
}
```

If no rules match, returns `{"flags": []}`.

## Errors
- **422** — request body missing `text` or malformed JSON.
- **400** — `text` longer than 50,000 characters (oversize protection).

## Rules
Static list defined in `app/flag_clauses.py:RULES`. Each rule has:
- `name` (string)
- `pattern` (regex, evaluated case-insensitive)
- `severity` (`info` | `warning` | `critical`)

Rules are evaluated in order; all matches are returned (no dedup, no short-circuit).

## Edge Cases
- Empty `text` → returns `{"flags": []}` (not an error).
- Unicode in `text` → must not crash the regex engine.
- Multiple matches of the same rule → return each occurrence.
- Overlapping rule matches → return all (no dedup).
- Whitespace-only `text` → returns `{"flags": []}`.

## Non-Goals
- No persistence.
- No authentication or authorization.
- No multi-language support (English only).
- No clause severity escalation based on surrounding context (just the rule's static severity).
- No streaming response.

## Success Criteria
- All tests in `tests/unit/` pass with `pytest -xvs`.
- All tests in `tests/integration/` pass against a live server.
- Adversarial pass (`/redteam`) surfaces no untested attack vectors.
- Cold-start latency under 1s; per-request latency under 200ms for a 5,000-char input.
