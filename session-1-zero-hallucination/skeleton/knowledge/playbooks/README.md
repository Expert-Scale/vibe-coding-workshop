# Playbooks

Drop your playbook documents here. Anything Claude Code can `Read`:

- Markdown (`.md`) — easiest to retrieve from
- Plain text (`.txt`)
- PDF (`.pdf`) — Claude Code reads PDFs natively
- CSV (`.csv`) for structured data alongside the clause-matrix

## What's a playbook?

A playbook is your team's accumulated wisdom on how to handle a type of work. For a contract-review agent: an NDA playbook, an MSA playbook, a SOW playbook. For a customer-support agent: an escalation playbook, a refund-policy doc, an SLA reference. For a recruiting agent: an interview-rubric doc, a comp-band sheet, an offer-template guide.

## Suggested structure per playbook

```markdown
# <Topic> Playbook

## When does this apply?
<scope>

## Standard positions
<your defaults — what we do unless there's a reason not to>

## Required carve-outs / non-negotiables
<things that always stay>

## When to escalate
<bullets — the things this playbook does NOT cover>
```

## Tip

Start with one playbook. Get the agent answering well from it. Then add more. Building five playbooks before testing leads to spec drift you won't notice until production.
