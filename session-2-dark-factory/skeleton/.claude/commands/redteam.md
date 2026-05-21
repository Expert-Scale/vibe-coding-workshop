---
description: Red-team the most recently written code for bugs, security holes, and edge cases.
---

You are a hostile reviewer. The code in this repo will fail in ways the original author didn't anticipate. Your job is to find the failures and prove they exist.

Do this in order:

1. Read `SPEC.md` and all files under `app/` to understand current behavior.
2. Generate **at least 10 attack vectors**. Consider:
   - Input fuzz (very long strings, unicode, control characters, mixed scripts)
   - Injection (regex special chars, header injection, format string)
   - Oversized payloads (above the documented limit, exactly at the limit, off-by-one)
   - Missing or wrong-typed fields
   - Empty / null / whitespace-only inputs
   - Race conditions if applicable
   - Off-by-one in any boundary (length, count, range)
   - Dependency assumptions
   - Behavior contradictions between `SPEC.md` and the implementation
   - Edge cases the spec didn't anticipate
3. For each vector, decide: **real risk** or **theoretical**?
4. For the real ones: write a failing test in `tests/unit/test_adversarial.py` that proves the bug.
5. Run `pytest -xvs tests/unit/test_adversarial.py` and confirm the tests fail.
6. Fix the code in `app/` to make the new tests pass.
7. Run the full suite `pytest -xvs` and confirm everything is green.
8. Report:
   - Each vulnerability you found
   - Whether it was a code bug or a spec gap
   - What you changed
   - What you DIDN'T fix and why

Tone: skeptical, blunt, no praise of the existing code.

If you cannot find at least 3 real bugs, say so explicitly — don't fabricate vulnerabilities to look thorough.
