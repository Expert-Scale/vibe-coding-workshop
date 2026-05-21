# The Trust Ladder — Cheat Sheet

| Rung | What | When to use |
|------|------|-------------|
| 1. Auto-complete | Model finishes your line | Trivial syntax, you're driving |
| 2. Suggestion | Model proposes a block | Boilerplate, you accept or reject |
| 3. Pair | Chat-driven, you steer | Most day-to-day work |
| 4. Loop | Spec → code → tests → self-heal | Well-specified small features |
| 5. Dark factory | Nested loops + adversarial pass | Solid spec, bounded surface area |

## Picking a Rung

- **Risk low + spec clear** → climb higher
- **Risk high + spec fuzzy** → stay lower
- **One-way doors** (prod migrations, destructive ops) → never above rung 3
- **Greenfield + small + reversible** → rung 5 is fine

## Climbing Safely

- Whitelist permissions narrowly in `.claude/settings.json`. Never `Bash(*)`.
- Read diffs after every edit (the `PostToolUse` git-diff-stat hook helps).
- Pause when you see test-gaming or `try/except` swallowing.
- Keep `SPEC.md` updated in the same edit as any behavior change.
- The model can run forever. You need to know when to stop and review.

## When You Get Stuck on a Higher Rung

- Drop one rung. Pair with the model on the broken section.
- Once unblocked, climb back up if the work warrants it.
- It's not a one-way ladder.
