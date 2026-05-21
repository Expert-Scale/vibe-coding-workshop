# Session 2 — From Auto-Complete to Dark Factory

The five-rung trust ladder, with concrete Claude Code primitives for climbing rungs 4 and 5:

1. **Auto-complete** — finishes your line.
2. **Suggestion** — proposes blocks.
3. **Pair** — chat-driven, you steer.
4. **Loop** — model writes spec → code → tests → fixes until green. *(`CLAUDE.md` rules + pre-authorized Bash)*
5. **Dark factory** — nested loops + adversarial pass. *(`.claude/commands/redteam.md` + hooks)*

## Folders

- **`sample/`** — A fully-built **Clause Flagging Agent** (FastAPI endpoint, unit + integration tests, `/redteam` slash command, hook recipes). Run `pytest` to see the tests pass, then `claude` to drive it as an agent.
- **`skeleton/`** — Same structure with the spec, code, and tests blanked out. The lesson is *the agent fills in the skeleton*. You drive the loop.

## Lesson Plan

See [`../vibe-coding-session-2-dark-factory.md`](../vibe-coding-session-2-dark-factory.md) at the repo root.

## Try It

```bash
cd sample
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -xvs                # unit + integration both pass
claude
```

Then in Claude Code:

- `/redteam` — runs the adversarial pass against the implementation.
- *"Add a new rule for 'most favored nation' clauses. Update SPEC.md, add a test, implement, run pytest."* — exercises the full inner loop.
- *"Boot the server and verify the integration tests pass against a live instance."* — exercises the outer loop.

## Try the Skeleton

```bash
cd skeleton
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
claude
```

Then: *"Read SPEC.md. Expand it into a full spec. Then implement it, write unit tests, run pytest, fix until green."* Watch the loop run.
