# Optional — Pipe Escalations to a Human

The `ESCALATE` keyword in your agent's output is enough on its own — anyone reading the transcript can spot it. This doc shows two ways to surface escalations automatically once you outgrow manual scanning.

## Approach A — Manual (start here)
Once per day, scan the transcript or grep for `ESCALATE`:
```bash
grep -A 6 "^ESCALATE" ~/.claude/projects/<your-project>/transcripts/*.jsonl
```

Most small teams never need anything fancier than this.

## Approach B — Slack Webhook on Session End
Set up an [incoming webhook](https://api.slack.com/messaging/webhooks) in your Slack workspace, then export it:

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
```

Add this to `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "tail -n 50 .claude/last-output.txt | grep -q '^ESCALATE' && curl -s -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Agent escalated — check the transcript.\"}' \"$SLACK_WEBHOOK_URL\""
          }
        ]
      }
    ]
  }
}
```

## Approach C — Email Digest
Replace the `curl` in Approach B with `mail -s "Agent escalation"` piping the matched lines to whoever triages.

## Privacy Note
Whatever channel you escalate to will receive contract paragraphs or other sensitive content verbatim. Make sure the destination is private and appropriately access-controlled.
