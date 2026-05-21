# Vibe Coding Workshop — Two Sessions, One Day

Companion repo for a same-day pair of 45-minute workshops on practical AI agents.

## What's Here

```
.
├── vibe-coding-session-1-zero-hallucination.md   ← Session 1 lesson plan
├── vibe-coding-session-2-dark-factory.md         ← Session 2 lesson plan
├── session-1-zero-hallucination/
│   ├── sample/      ← Worked example — what you build live in session 1
│   └── skeleton/    ← Empty framework — clone, fill in, ship
└── session-2-dark-factory/
    ├── sample/      ← Worked example — what you build live in session 2
    └── skeleton/    ← Empty framework — clone, fill in, ship
```

## The Two Sessions

**Session 1 — Zero-Hallucination AI Agents.** For everyone, leaning non-technical. Four guardrails that turn a confidently-wrong LLM into a useful agent: Context, Memory, KB-First, Bounded. The worked example is a **Contract Review Agent**.

**Session 2 — From Auto-Complete to Dark Factory.** For technical attendees. The five-rung trust ladder, climbed by letting the model write the spec, code, tests, integration tests, and red-team its own work. The worked example is a **Clause Flagging Agent** (FastAPI endpoint).

Both sessions use Claude Code as the demo environment. The architecture and rules translate to any agent stack.

## How to Use This Repo

- **Following along at the workshop?** Clone the repo, open the matching `skeleton/` folder, and work the lesson plan top-to-bottom. The skeleton has the same structure as the sample with the rules and content blanked out.
- **Back at the office?** Open the matching `sample/` folder to see the finished version, then copy `skeleton/` into your own project and adapt the markdown to your domain.
- **Just reading?** Start with the lesson plan markdown at the root, then peek at the `sample/` folders to see what each guardrail looks like as files.

## Prerequisites

- [Claude Code](https://www.anthropic.com/claude-code) installed (one-line install per session SETUP.md)
- A Claude.ai account
- Session 2 only: Python 3.10+

## Quick Start

```bash
# Session 1
cd session-1-zero-hallucination/sample
claude
# Try: "What's a reasonable indemnity cap for a SaaS vendor with a $200k ACV?"

# Session 2
cd session-2-dark-factory/sample
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -xvs
claude
# Try: /redteam
```

## License

MIT — use, adapt, ship. Just don't claim it as your own teaching material verbatim.
