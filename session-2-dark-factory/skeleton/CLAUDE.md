# <!-- TODO: Feature name --> — Working Rules

## Spec Discipline
- `SPEC.md` is the source of truth for this feature.
- Any change to behavior MUST update `SPEC.md` in the same edit.
- If the spec is unclear, ASK before coding.

## Inner Loop Rules
- Every implementation gets unit tests in the same change.
- After writing tests, RUN them via the Bash tool: `pytest -xvs tests/unit/`.
- If a test fails, fix the CODE — not the test — unless the test itself is genuinely wrong, in which case explain why before changing it.
- Continue until tests pass. Then stop and report.
- Use the TodoWrite tool to track each step.

## Outer Loop Rules
- Integration tests live in `tests/integration/` and exercise the feature end-to-end.
- NEVER use a broad `try/except` to silence errors. Find the root cause.
- If something won't boot or run, read the actual error before "fixing" anything.

## Adversarial Pass
- Run `/redteam` to red-team the latest implementation.
- The red-team agent should find at least 5 real attack vectors, write failing tests for them in `tests/unit/test_adversarial.py`, then fix the code.

## What Not to Do
- Don't add broad `try/except` to make failures vanish.
- Don't add `pytest.skip` without explaining why.
- Don't install packages without asking first.
- Don't claim "done" until you've pasted actual passing test output.
- Don't edit `SPEC.md` and code in two separate commits — they go together.

<!-- This file is the same architecture as the sample. The only thing you may want
to change is the feature name in the title. Everything else is universal. -->
