# Setup — Skeleton

This is the empty framework. Clone it, fill in the TODO blocks, point it at your own knowledge, and you have an agent.

## Prerequisites
- Node.js 18+
- A Claude.ai account

## Install Claude Code
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

## Fill It In (the order matters)

1. **`CLAUDE.md`** — Edit each `<!-- TODO -->` block. Start with the Role + Interview questions. Save.
2. **`memory/red-flags.md`** — List the patterns that should halt the agent for your domain.
3. **`memory/green-flags.md`** — List the signals that the conversation is on track.
4. **`knowledge/clause-matrix.csv`** (or rename it) — Add structured rows of "if input matches X, answer is Y." Start with 5-10 rows.
5. **`knowledge/playbooks/`** — Drop your playbook documents in here. Markdown, PDF, text — anything Claude Code can `Read`.
6. **`ESCALATE-HOOK.md`** — Optional. Set up Slack/email piping if you want automated escalation.

## Run It
```bash
claude
```

## Try It

Ask a question that should hit your knowledge base:
> *Your test prompt here, e.g. "What's our standard NDA term length?"*

Then ask one that's out of scope:
> *Your out-of-scope prompt, e.g. "Can you draft a termination notice?"*

The first should cite a file. The second should return the `ESCALATE` block.

## Adapt Further

The four guardrails (Interview, Memory, KB, Fence) are the architecture. Everything else is content. Change the role, the interview questions, the red flags, the knowledge — but keep the structure of `CLAUDE.md` intact.
