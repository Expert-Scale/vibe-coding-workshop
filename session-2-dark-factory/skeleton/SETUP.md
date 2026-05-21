# Setup — Skeleton

This is the empty framework. You're going to let Claude Code fill most of it in.

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
cd session-2-dark-factory/skeleton
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Drive the Loop

1. Open `SPEC.md`. Replace the intent block (4-5 lines) with what you want to build.
2. Start Claude Code:
   ```bash
   claude
   ```
3. Ask:
   > *Read SPEC.md. Enter plan mode. Expand the intent into a rigorous spec with request/response schema, errors, edge cases, non-goals, and success criteria. Do not write code yet.*
4. Review and edit the expanded spec. Save.
5. Ask:
   > *Implement SPEC.md in `app/`. Write unit tests in `tests/unit/`. Run pytest. Fix until green.*
6. Watch the loop. Interrupt when you see the model fixing tests instead of code, or wrapping failures in `try/except`.
7. Once green, ask:
   > *Write integration tests in `tests/integration/` that exercise the feature end-to-end. Run them. Fix until green.*
8. Finally:
   > */redteam*
9. Review the diff. Commit.

## What's Provided

- `CLAUDE.md` — the rules that govern the loop
- `SPEC.md` — intent stub
- `.claude/settings.json` — permission whitelist + diff hook
- `.claude/commands/redteam.md` — adversarial pass slash command
- `requirements.txt` — minimal Python deps
- `app/__init__.py` — empty package
- `app/PLACEHOLDER.md` — the agent replaces this with implementation files
- `tests/unit/README.md` and `tests/integration/README.md` — the agent fills these dirs

## What's NOT Provided

- Any actual implementation
- Any tests

That's the point. The lesson is letting the agent build it.
