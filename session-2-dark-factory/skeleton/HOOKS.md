# Hook Recipes

Hooks live in `.claude/settings.json` and fire on specific events during a Claude Code session.

The skeleton's `.claude/settings.json` already includes one hook: **diff-on-edit**. Add others as you grow.

## Diff-on-Edit (already enabled in this skeleton)

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

## Test-on-Stop

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

## Dep-Add Warning

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

Start with one. Add more only when you feel the pain.
