# Session 1 — Zero-Hallucination AI Agents

The four guardrails that keep an LLM-backed agent from confidently lying:

1. **Context** — Ask before answering. (`CLAUDE.md` "Interview First" block)
2. **Memory** — Remember and flag. (`memory/red-flags.md`, `memory/green-flags.md`)
3. **KB-First** — Answer from your own materials. (`knowledge/` folder + CSV + playbooks)
4. **Bounded** — Escalate when outside. (`CLAUDE.md` "Fence" block)

## Folders

- **`sample/`** — A fully-built Contract Review Agent. Run `claude` inside it to see all four guardrails working. Read `CLAUDE.md` to see how each guardrail is wired in.
- **`skeleton/`** — Same structure with the content blanked out. Clone this into your own project and fill it in for your domain.

## Lesson Plan

See [`../vibe-coding-session-1-zero-hallucination.md`](../vibe-coding-session-1-zero-hallucination.md) at the repo root.

## Try It

```bash
cd sample
claude
```

Then ask:

1. *"What's a reasonable indemnity cap for a SaaS vendor with a $200k ACV?"*
   → It should ask follow-up questions, then quote the row from `knowledge/clause-matrix.csv`.

2. *"Review this clause: 'Vendor accepts unlimited liability for all damages.'"*
   → It should match a red flag and halt with an escalation.

3. *"Can you draft me a termination notice?"*
   → It should return the `ESCALATE` block instead of drafting.
