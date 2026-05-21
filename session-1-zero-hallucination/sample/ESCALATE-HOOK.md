# Optional — Pipe Escalations to a Human

The agent's `ESCALATE` block is already useful as-is — anyone reading the transcript can spot it. This doc shows two ways to surface escalations automatically.

## Approach A — Manual (start here)
Have the agent always include `ESCALATE` at the top of its escalation message (already wired in `CLAUDE.md`).

Once per day, run:
```bash
grep -A 6 "^ESCALATE" ~/.claude/projects/<your-project>/transcripts/*.jsonl
```

…or just scan the transcript. Most small teams never need anything fancier than this.

## Approach B — Slack Webhook on Session End
Add a Slack incoming-webhook URL to your environment:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

Then add this to `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "tail -n 50 .claude/last-output.txt | grep -q '^ESCALATE' && curl -s -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Contract agent escalated. Check the transcript.\"}' \"$SLACK_WEBHOOK_URL\""
          }
        ]
      }
    ]
  }
}
```

(You'll need to capture the agent's final response to `.claude/last-output.txt` first — recipe in the workshop repo's HOOKS notes. The point is the *pattern*: detect the keyword, ping the human.)

## Approach C — Email Digest
Replace the `curl` in Approach B with `mail -s "Contract review escalation"` piping the matched lines to whoever triages.

## A Note on Privacy
Whatever channel you escalate to, the agent will quote contract paragraphs verbatim. Make sure the destination is appropriate for that content — a private Slack channel, an internal email list, not a public room.
