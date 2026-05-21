# Hook Recipes

Hooks live in `.claude/settings.json` and fire on specific events during a Claude Code session. Use them to catch the failure modes of higher-rung work — stealth dependencies, silent edits, broken tests — automatically.

## Diff-on-Edit (always know what changed)

After every `Edit` or `Write`, print a diff stat to the terminal:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "git diff --stat" }
        ]
      }
    ]
  }
}
```

**Why:** sprawling changes and stealth dependency adds become impossible to miss.

## Lint-on-Write

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": "ruff check app/ || true" }
        ]
      }
    ]
  }
}
```

**Why:** lint feedback is faster than a test run. Catches obvious issues before the next loop.

## Test-on-Stop (run tests when the agent finishes a turn)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "pytest -x --tb=short" }
        ]
      }
    ]
  }
}
```

**Why:** confirms the agent's "done" claim with actual passing tests. Catches "confidence inflation."

**Caution:** fires every turn. Noisy during long sessions. Start with one hook, add more only when you feel the pain.

## Dep-Add Warning

If you do allow `Bash(pip install:*)`, log every install:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "grep -E '(pip|npm|yarn|poetry) (install|add)' && echo '⚠️  Dependency change incoming' || true" }
        ]
      }
    ]
  }
}
```

**Why:** "silent dependencies" are the #1 dark-factory failure mode. Make them loud.

## Combining Hooks

You can stack multiple matchers in the same `PostToolUse` array. Order doesn't strictly matter for output, but keep fast checks (lint) before slow ones (test).
