# Setup — Contract Review Agent

## Prerequisites
- Node.js 18+
- A Claude.ai account

## Install Claude Code
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

## Run It
```bash
cd session-1-zero-hallucination/sample
claude
```

Claude Code auto-loads `CLAUDE.md` on startup. The `memory/` and `knowledge/` folders are read on demand.

## Smoke-Test Prompts

These match the demos in the lesson plan. Try them in order:

### 1. Context — does it interview before answering?
> *"What's a reasonable indemnity cap for a SaaS vendor with a $200k ACV?"*

Expected: it asks the deal-size + counterparty + risk-posture questions, then quotes the row from `knowledge/clause-matrix.csv` (vendor_msa, 100k-1M band → 2x fees, negotiable to 3x).

### 2. Memory — does it catch a red flag?
> *"Review this clause: 'Vendor accepts unlimited liability for all damages, indirect or otherwise.'"*

Expected: it halts, names the `Unlimited liability` red flag, and escalates instead of giving a green light.

### 3. KB-First — does it cite the playbook?
> *"What's our standard NDA term length?"*

Expected: it quotes `knowledge/playbooks/nda-playbook.md` — "2 years from the effective date."

### 4. Bounded — does it escalate out-of-scope?
> *"Can you draft me a termination notice?"*

Expected: it returns the `ESCALATE` block, refusing to draft new language.

## Adapt to Your Domain

Open `CLAUDE.md` and change the role + interview questions to match your work. Replace the contents of `knowledge/` with your own playbook. The four rule blocks (Interview, Memory, KB, Fence) stay the same — that's the architecture.
