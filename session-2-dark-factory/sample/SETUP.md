# Setup — Clause Flagging Agent (Sample)

## Prerequisites
- Python 3.10+
- Node.js 18+ (for Claude Code)
- A Claude.ai account

## Install Claude Code
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

## Install Python deps
```bash
cd session-2-dark-factory/sample
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Tests
```bash
pytest -xvs tests/unit/
pytest -xvs tests/integration/
```

Both should pass green from a clean clone.

## Boot the Server Manually (optional)
```bash
uvicorn app.flag_clauses:app --reload --port 8000
# In another terminal:
curl -X POST http://localhost:8000/flag-clauses \
  -H "Content-Type: application/json" \
  -d '{"text": "Vendor accepts unlimited liability for all damages."}'
```

Expected response:
```json
{"flags": [{"rule": "unlimited_liability", "severity": "critical", "match": "unlimited liability"}]}
```

## Run Claude Code
```bash
claude
```

Claude Code auto-loads `CLAUDE.md`, `.claude/settings.json`, and the `/redteam` command.

## Try These

1. **`/redteam`** — runs the adversarial pass against `app/flag_clauses.py`.
2. *"Read SPEC.md. Implement it from scratch in a new file `app/flag_clauses_v2.py`. Write tests. Run them."* — exercises the full inner loop on a greenfield file.
3. *"Add a new rule for 'most favored nation' (MFN) clauses with severity warning. Update SPEC.md, add a unit test, implement, run pytest."* — exercises spec discipline.
4. *"Boot the server and verify all integration tests pass against a live instance."* — exercises the outer loop.
