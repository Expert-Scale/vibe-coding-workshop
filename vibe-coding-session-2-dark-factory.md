# Vibe Coding Session 2 — From Auto-Complete to Dark Factory

**Audience:** Advanced / technical attendees. Comfortable in a terminal, have used Copilot or Cursor, may have written a basic agent.
**Format:** 45 min, live build of one small feature with the model doing 80%+ of the work — spec, code, tests, fixes, adversarial review. **Teach-and-show**: every section includes a step-by-step DIY block they can run at the office Monday.
**Companion:** Session 1 (Zero-Hallucination AI Agents) was the *consumer* side — how to keep a model honest. Session 2 is the *builder* side — how to let it do more without losing control.
**Tooling:** **Claude Code** throughout. Same primitives translate to Cursor agent mode, Aider, or your own loop — Claude Code just makes the rungs the easiest to demonstrate.
**Take-home repo:** https://github.com/expertscale/vibe-coding-workshop

---

## The One Big Idea

Session 1: *trust the model less.*
Session 2: *trust the model more — at the right rungs.*

Most engineers are using AI as **enhanced auto-complete**. There are five rungs above that, and the higher rungs ship features in minutes instead of hours. The skill we're teaching today is knowing which rung is safe for which kind of work — and how to set up Claude Code so each rung is a single command away.

---

## The Trust Ladder

1. **Auto-complete** — finishes your line. You drive.
2. **Suggestion** — proposes blocks. You accept or reject.
3. **Pair** — chat-driven; model writes, you steer.
4. **Loop** — model writes spec → code → tests → fixes itself until green.
5. **Dark factory** — nested loops; model writes, tests, integration-tests, then red-teams its own output. You review the final diff.

Most teams stop at rung 3. Today we climb to 4 and 5.

---

## The Running Example

Build a small **clause-flagging agent**: an endpoint that takes a contract paragraph and returns flagged clauses with severity. Small enough to finish in 30 minutes, real enough to have edge cases, adversarial enough to red-team. (Swap in any small agent if the room would connect better with a different domain — the loop is what we're teaching.)

---

## Time Budget

| Time | Block |
|------|-------|
| 0:00–0:05 | Hook + the ladder |
| 0:05–0:12 | Spec-first |
| 0:12–0:22 | Code + unit tests + self-heal |
| 0:22–0:32 | Integration tests + self-heal |
| 0:32–0:40 | Adversarial pass |
| 0:40–0:45 | Where it breaks + close |

---

## 0:00–0:05 — Hook + The Ladder

Show a Copilot tab completion in your editor. *"This is where most of you stop."* Close it. Open a terminal with Claude Code running. *"Here's where we're going."*

Walk the 5 rungs. Be blunt: every rung is a choice about trust. Higher rungs are dramatically faster but punish you harder when they go wrong. Today's job is to feel where the edge is — and to see the exact Claude Code primitives that let you climb each rung safely.

### DIY: One-Time Setup

If attendees want to follow along, this is the install + permission scoping you do once:

```bash
# 1. Install + login
npm install -g @anthropic-ai/claude-code
claude login

# 2. In your project folder, create the basics:
mkdir -p .claude
touch CLAUDE.md SPEC.md
```

Pre-authorize the tools your loop will use so it doesn't stop every 30 seconds asking for permission. In **`.claude/settings.json`**:

```json
{
  "permissions": {
    "allow": [
      "Bash(pytest:*)",
      "Bash(npm test:*)",
      "Bash(curl:*)",
      "Bash(uvicorn:*)",
      "Read(./**)",
      "Write(./**)",
      "Edit(./**)"
    ]
  }
}
```

> Whitelist narrow. Never `Bash(*)`. The point is to grant the loop autonomy *within a fence* — same principle as session 1's KB fence, one layer down.

---

## 0:05–0:12 — Spec-First

You don't write code. You write **intent** — 4–5 lines describing what the feature does. Then hand it to the model and ask it to draft a rigorous spec: explicit inputs, outputs, error cases, edge cases, non-goals.

Edit one thing it got wrong on screen. Commit the spec as a file in the repo.

**Why this rung works:** specs are cheap to fix. Code generated from a wrong spec is expensive to fix.

### DIY: Spec-First in Claude Code

1. Open `SPEC.md`. Paste 4–5 lines of intent:

   ```markdown
   # Intent
   POST /flag-clauses takes a contract paragraph and returns a list of flagged
   clauses with severity (info|warning|critical). Flags come from a static
   ruleset. Latency target <200ms. JSON in, JSON out. No DB.
   ```

2. **Enter plan mode** — press `Shift+Tab` until you see "plan mode" in the footer. Plan mode forces Claude to design before editing.

3. Ask:

   > *Read SPEC.md. Expand it into a full spec: explicit request/response schema, error cases, edge cases, non-goals, success criteria. Use the same file. Do NOT write code.*

4. When it returns the expanded spec, **read it on screen out loud**. Edit one thing it got wrong — point at it: *"This is where the spec round catches what a bad code round can't."*

5. Save. Commit. The spec is now your contract for the rest of the session.

**Pro move:** Add this to **`CLAUDE.md`**:

```markdown
# Spec Discipline
- SPEC.md is the source of truth for this feature.
- Any change to behavior MUST update SPEC.md in the same edit.
- If the spec is unclear, ASK before coding.
```

This single rule prevents 80% of spec drift later.

---

## 0:12–0:22 — Code + Unit Tests + Self-Heal *(the inner loop)*

Hand the spec back: *"Implement SPEC.md. Write unit tests that prove it. Run them with pytest. If anything fails, fix the code and re-run until green."*

Watch the loop run live:
- Implementation appears
- Unit tests appear
- Tests run
- Something fails
- Model diagnoses, edits, re-runs
- Green

**Where to interrupt:** when the model "fixes" the test instead of the code. That's the most common failure mode at this rung. Catch it on screen so the room sees what to look for.

### DIY: The Inner Loop in Claude Code

1. Add to **`CLAUDE.md`**:

   ```markdown
   # Inner Loop Rules
   - Every implementation gets unit tests in the same change.
   - After writing tests, RUN them via the Bash tool (pytest -xvs).
   - If a test fails, fix the CODE — not the test — unless the test itself is wrong, in which case explain why before changing it.
   - Continue until tests pass. Then stop and report.
   - Use TodoWrite to track each step so the user can see where you are.
   ```

2. Kick off the loop:

   > *Read SPEC.md. Implement it in `app/flag_clauses.py`. Write unit tests in `tests/unit/test_flag_clauses.py`. Run pytest. Fix until green. Don't ask me between steps.*

3. **Watch for these failure moments and pause the loop:**
   - Model edits the assertion to match the broken output → *"No. Fix the code."*
   - Model adds a `pytest.skip` → *"No. Make the test pass for real."*
   - Model silently drops a test → *"No. Why was that test there? Restore it and address the root cause."*

4. When green, ask the model to summarize what it changed and why — 3 bullets max. Commit.

**Why pre-approved Bash matters:** without it, the model stops after every `pytest` to ask permission. With it, the loop actually loops.

---

## 0:22–0:32 — Integration Tests + Self-Heal *(the outer loop)*

Now raise the bar: *"Write a scenario test that calls the endpoint over HTTP end-to-end. Boot the server. Run it. Fix anything that breaks until it passes."*

New failure surface: env vars, port collisions, missing fixtures, real I/O. Same loop, bigger scope. Let the model thrash a little — that's part of the lesson.

**Where to interrupt:** when the model adds a broad `try/except` to make a failure vanish instead of diagnosing the root cause. Stop it. Tell it to find the actual cause. Show the room what *not* to let through.

### DIY: The Outer Loop in Claude Code

1. Add to **`CLAUDE.md`**:

   ```markdown
   # Outer Loop Rules
   - Integration tests live in tests/integration/ and exercise the endpoint over HTTP.
   - To run: boot the server in the background with uvicorn, hit it with curl or httpx, assert on the response.
   - NEVER use a broad try/except to silence errors. If a test fails, find the root cause.
   - If the server won't boot, read the actual error before "fixing" anything.
   ```

2. Kick off:

   > *Write tests/integration/test_flag_clauses_http.py that boots the app and hits POST /flag-clauses with a real contract paragraph. Run it. Fix until green.*

3. **Watch for these moments:**
   - Model wraps a network call in `try: ... except: pass` → *"Stop. What error did you actually see? Print it. Fix the cause."*
   - Model adds `time.sleep(5)` to "wait for the server" → *"That's a smell. Use a readiness check."*
   - Model hardcodes a port that's already in use → *"Read the error. Fix it properly — bind to 0 or read from env."*

4. When green: have the model update SPEC.md with anything the integration test surfaced that the spec missed (rate limit behavior, error responses, etc.). This is how you fight spec drift.

---

## 0:32–0:40 — Adversarial Pass

The rung most teams never climb. Tell the model to red-team its own code: input fuzz, injection, race conditions, malformed contracts, oversized payloads, bad encoding. List the real ones. Add tests. Fix the code.

You'll have one bug pre-staged in case the live model doesn't bite — but in my experience it bites about 80% of the time. The same model that wrote the code, in adversarial mode, catches a surprising amount of its own work.

**Why this rung works:** the bias that produced the bug isn't active when the model is hunting for bugs. Two different "modes," same model.

### DIY: The Adversarial Pass in Claude Code

There are two clean ways to do this. Show one live; mention the other.

**Option A — A custom `/redteam` slash command.** Create **`.claude/commands/redteam.md`**:

```markdown
---
description: Red-team the most recently written code for bugs, security holes, and edge cases.
---

You are a hostile reviewer. The code I just wrote will fail in ways I didn't anticipate.

Do this:
1. Read SPEC.md and the most recent implementation files.
2. Generate at least 10 attack vectors: input fuzz, injection, oversized payloads,
   unicode/encoding edge cases, race conditions, missing fields, wrong types,
   off-by-one in any boundary, dependency assumptions that may not hold.
3. For each, decide: real risk or theoretical?
4. For the real ones: add a failing test that proves the bug exists.
5. After tests confirm the bugs, fix the code. Re-run all tests. Report what you found.

Tone: skeptical, blunt, no praise of the existing code. Your job is to break it.
```

Then in the session: `/redteam` and let it run.

**Option B — Spawn a subagent.** In the main session ask:

> *Use the Agent tool to launch a general-purpose agent with this brief: "Red-team the code in app/flag_clauses.py against SPEC.md. Find real bugs, write failing tests for them, then fix the code. Report findings."*

Subagent gets a fresh context — even less likely to defend its own prior work.

**Pre-stage a bug** (in case the live pass misses): a regex that matches "indemnity" but not "indemnification". Confirm offline that the red-team pass catches it. If live catches something better, drop the pre-staged one.

---

## 0:40–0:45 — Where It Breaks + Close

Be honest about the failure modes of the dark-factory rung:

- **Spec drift** — model updates code, forgets to update SPEC.md. *Mitigation:* the CLAUDE.md rule in Pillar 1, plus diffing SPEC.md every commit.
- **Test gaming** — writes tests that pass instead of tests that prove. *Mitigation:* read tests before you read code; interrupt when assertions match broken output.
- **Confidence inflation** — claims "done" before it's done. *Mitigation:* require the model to run the tests and paste the actual output, not summarize.
- **Silent dependencies** — installs packages without telling you. *Mitigation:* don't whitelist `Bash(pip install:*)` or `Bash(npm install:*)` in `.claude/settings.json` — keep installs gated.

The pattern across all four: **short loops, frequent diffs, narrow permissions, a human reading the changes before the next loop starts.** You're not removing yourself — you're moving up the stack.

### DIY: One Hook to Catch the Worst Failure Modes

Add to **`.claude/settings.json`** (optional, but powerful):

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

Every edit prints a diff stat to your terminal. You can't miss a stealth dependency add or a sprawling change. (More hook recipes in the repo.)

Closing line:

> *Session 1 was about teaching an agent where its lane is. Session 2 is about giving the agent the keys inside that lane. The skill is knowing which side of the line you're on at any given moment.*

Open Q&A. Share the GitHub repo + the spec template.

---

## What's in the Take-Home Repo

Spell this out on the last slide:

- This lesson plan as a markdown doc
- A starter `CLAUDE.md` with the inner-loop, outer-loop, and spec-discipline rule blocks
- A `SPEC.md` template (intent block + expandable sections)
- A starter `.claude/settings.json` with safe permission scoping
- The `/redteam` slash command at `.claude/commands/redteam.md`
- A hook recipe collection (`HOOKS.md`) — git-diff-on-edit, lint-on-write, test-on-stop
- The clause-flagging agent we built today as the worked example
- A `LADDER.md` cheat-sheet — when to use each rung

---

## Pre-Flight (instructor)

- Two-pane setup: Claude Code on the left, file diff or test output on the right. Font bumped.
- Clean repo pre-cloned, dependencies installed, server bootable in one command. Practice the cold start before the room arrives.
- `.claude/settings.json` pre-loaded with the permission whitelist — *do not* leave Claude pausing for permission every 30 seconds during the live loop.
- The `/redteam` command already saved.
- One pre-staged bug ready (regex that misses "indemnification") in case live adversarial pass comes up empty.
- API key + a hard token budget. Loops burn tokens — `claude config` it before the workshop.
- GitHub repo public + URL on a sticky note for the wrap.

## Pre-Flight (attendees who want to follow along)

> *"You don't need to follow along live — the repo has everything we touch. If you do want to follow, install Claude Code now (link in chat) and clone the starter repo. The first 5 minutes of setup will track what I'm showing."*
