# Zero-Hallucination AI Agents — 45-Minute Workshop Plan

**Format:** Live "vibe coding" — build a working legal-playbook agent on screen while teaching the 4 guardrails. **Teach-and-show**: every section gives attendees a step-by-step they can repeat at the office on Monday.
**Audience note:** Mixed room, leaning non-technical. One known attendee (Mona, ACP / in-house legal team of one) wants to build a contract-review playbook + provisions FAQ + assistant agent. **Tune every example to that use case.**
**Reference diagram:** `https://apexreplicant.ai/presentations/investment/images/zeroHal.png` *(labels say "expert" / "client" — read them as "agent owner" / "user"; the architecture is the same)*
**Take-home repo:** https://github.com/Expert-Scale/vibe-coding-workshop

---

## The One Big Idea

Most AI tools jump straight to answering. We're going to teach the model to **understand first, answer only from validated sources, and escalate when it's outside its lane.** That's the difference between a confident liar and a useful agent.

Four guardrails. One running example: a **Contract Review Agent** that helps Mona's team triage NDAs and MSAs before outside counsel touches them.

**Tools used today:**
- **Vanilla Gemini Flash + ChatGPT** — for the opening "watch it hallucinate" demo only
- **Claude Code** — for the rest of the session (where we actually build the agent)

> The architecture works with any model. Claude Code is just the fastest way to *show* it on a laptop. The same patterns translate to Gemini, GPT, or whatever your office already pays for.

---

## Time Budget

| Time | Block |
|------|-------|
| 0:00–0:04 | Hook — vanilla LLMs hallucinate (Gemini Flash + ChatGPT) |
| 0:04–0:06 | Switch to Claude Code — quick orientation |
| 0:06–0:14 | Pillar 1 — Context |
| 0:14–0:22 | Pillar 2 — Memory |
| 0:22–0:33 | Pillar 3 — Knowledge Base First |
| 0:33–0:40 | Pillar 4 — Bounded / Escalate |
| 0:40–0:45 | Wrap + Q&A + repo link |

---

## 0:00–0:04 — Hook: Watch Vanilla LLMs Hallucinate

**Do this live on screen, side by side if possible:**

1. Open **gemini.google.com** in one tab (Gemini Flash, default settings).
2. Open **chat.openai.com** in another tab (free ChatGPT).
3. Ask both the *same* question: *"What's a reasonable indemnity cap for a SaaS vendor with a $200k ACV?"*
4. Read the answers out loud. Both will produce a confident, specific number — pulled from nowhere in particular. Maybe they'll disagree with each other. That's the point.

**The narration:**

> Notice what they didn't do. They didn't ask who's the counterparty. They didn't ask about your company's risk posture. They didn't cite a playbook. They didn't say "I don't know." That last one is the most expensive missing feature in AI today — and we're going to add it.

Then walk the diagram once, naming the 4 guardrails: **Context → Memory → KB-First → Bounded.** Tell the room: every step we take from here plugs into one of these four boxes.

---

## 0:04–0:06 — Switch to Claude Code (Quick Orientation)

**Close the browser tabs. Open a terminal.**

> *"For the rest of this session I'm using Claude Code. It's a command-line AI agent from Anthropic — think 'the AI runs in your terminal, on your files, with rules you set.' I'm using it because it makes today's lesson trivial to show. The same architecture works in Gemini or ChatGPT — Claude Code just makes the wrapper visible."*

Show three things on screen:

1. `claude` command running — a blank session.
2. A `CLAUDE.md` file open in your editor. *"This is where the agent gets its rules — like a job description."*
3. A `knowledge/` folder. *"This is where Mona's playbook docs and clause matrix will live."*

**DIY (in the repo README):**

```
1. Install Claude Code:  npm install -g @anthropic-ai/claude-code  (or the latest install path)
2. Sign in:  claude login
3. cd into any folder.  Run:  claude
4. Create a CLAUDE.md file — anything you write here, the agent reads on every turn.
5. Create a knowledge/ folder — drop your docs in there.
```

That's the whole setup. Now we build the four guardrails on top.

---

## 0:06–0:14 — Pillar 1: Context

> Before answering anything, ask: *do I actually understand what you need?*

The four moves (Mona's whiteboard 1A-D):

- **1st Prompt** — A system prompt that names the agent's job: *"You help in-house legal triage contracts before outside counsel. You ask before you answer."*
- **Interview** — A short set of questions the agent must ask before giving advice: *What kind of contract? Who's the counterparty? What's the dollar exposure? What's your company's risk posture?*
- **Active Listening** — A self-check before any answer: *Do I have enough to answer accurately, or do I need to ask one more question?* If unsure, ask. Loop.
- **Tone** — One line in the system prompt locks the voice. For Mona: *"warm, plain-language, never lawyerly with non-lawyers."*

**Demo:** Re-run the indemnity-cap question. This time the agent asks *"What's the deal size and what's the vendor's insurance floor?"* instead of guessing.

### DIY: Set This Up in Claude Code

1. In your project folder, open **`CLAUDE.md`**.
2. Paste a block like this (edit for your domain):

   ```markdown
   # Role
   You are a contract review assistant for an in-house legal team of one.
   You help triage NDAs and MSAs before outside counsel is engaged.

   # Interview First — Always
   Before giving any answer, you MUST confirm:
   1. What kind of contract is this? (NDA, MSA, SOW, vendor, customer)
   2. Who is the counterparty?
   3. What is the dollar exposure?
   4. What is our risk posture on this deal? (high / medium / low)

   If any of these are unclear, ask ONE question to clarify. Do not answer yet.

   # Tone
   Plain language. Warm. Never lawyerly with non-lawyers.
   Short sentences. Cite the playbook when you can.
   ```

3. Save. Restart the agent (or just keep going — Claude Code picks `CLAUDE.md` up).
4. Test: ask the indemnity-cap question. It should now ask back instead of answering.

**Takeaway:** Forcing the model to confirm context kills most hallucinations before they happen. The whole setup is one markdown file.

---

## 0:14–0:22 — Pillar 2: Memory

> Remember what you were just told. Notice patterns that change the answer.

Three pieces (Mona's 2A-C):

- **History** — Every turn of the conversation is fed back into the next prompt. Claude Code does this automatically inside one session.
- **Red Flags** — Patterns that should *change* behavior. For Mona: *counterparty asking for unlimited liability, NDA signed before scope is defined, indemnity one-way against us.* Each one triggers "flag this for human review."
- **Green Flags** — Signals the conversation is on track. User providing specifics, asking deeper follow-ups, confirming understanding. Feed those back so the agent stays in that mode.

**Demo:** Paste a one-paragraph NDA clause with a buried "unlimited liability" phrase. The agent catches it, says *"this one needs Mona's eyes — here's why,"* and stops.

### DIY: Set This Up in Claude Code

1. In your project folder, create **`memory/red-flags.md`**:

   ```markdown
   # Red Flags — Halt and Escalate
   - Unlimited liability (any direction)
   - Indemnity one-way against us
   - NDA signed before scope defined
   - Auto-renewal beyond 12 months without notice window
   - Governing law outside US/UK
   ```

2. Create **`memory/green-flags.md`**:

   ```markdown
   # Green Flags — Keep Going
   - User providing specific deal facts (counterparty, $, dates)
   - User asking "why" follow-ups
   - User confirming understanding before moving on
   ```

3. Add this to **`CLAUDE.md`**:

   ```markdown
   # Memory Rules
   - Before every answer, scan the user's message against memory/red-flags.md.
     If you match a red flag, STOP, explain which one, and escalate.
   - Track green flags silently — they tell you the conversation is healthy.
   ```

4. For longer-term memory across sessions, use Claude Code's built-in `/remember` command — it saves facts that persist between conversations.
5. Test: paste a clause with one of the red-flag phrases. It should halt.

**Takeaway:** Memory isn't just transcript. It's pattern-matching against things you've decided matter. Two markdown files and a rule in `CLAUDE.md` get you 80% of the value.

---

## 0:22–0:33 — Pillar 3: Knowledge Base First *(biggest section — slow down here)*

> Don't ask the LLM what it thinks. Ask your own materials first. The model only fills in the gaps.

Three places knowledge lives — work them in this order:

1. **Structured (rows in a table)** — Things with definitive answers. For Mona: a **clause matrix** — counterparty type × clause type × our standard position. *"For a vendor under $100k, our standard indemnity cap is 1x fees."* Pull the row. Done. No LLM creativity needed.
2. **Documents (your actual files)** — The playbook docs, past contracts, redline guides.
3. **Semantic search (RAG)** — Fuzzy, meaning-based search across the same documents when the user's question doesn't match a clean lookup.

**Order matters.** Cheap and precise first, fuzzy last. Most teams skip straight to step 3 and wonder why the answers are mushy.

**Demo:** Ask the agent a question that has a clear answer in the clause matrix. It pulls the row and cites the file path. Then ask a fuzzy one — *"What's our usual stance on AI-training clauses?"* — and it falls through to document search.

### DIY: Set This Up in Claude Code

1. Create a **`knowledge/`** folder. Inside it:

   ```
   knowledge/
     clause-matrix.csv         ← structured (Pillar 3a)
     playbooks/
       nda-playbook.md         ← documents (Pillar 3b)
       msa-playbook.md
       redline-guide.md
     past-contracts/           ← documents (Pillar 3b)
   ```

2. Build `clause-matrix.csv` with columns like:

   ```
   contract_type,clause,our_standard_position,deal_size_band,notes
   vendor_msa,indemnity_cap,1x_fees,<100k,boilerplate
   vendor_msa,indemnity_cap,2x_fees,100k-1M,negotiable to 3x
   nda,term_length,2_years,any,non-negotiable
   ```

3. Add this to **`CLAUDE.md`**:

   ```markdown
   # Knowledge Base Rules — Search In This Order
   1. FIRST: read knowledge/clause-matrix.csv. If the question matches a row exactly, quote it and stop.
   2. SECOND: search knowledge/playbooks/ for relevant passages. Quote the file path + the passage verbatim.
   3. THIRD: search knowledge/past-contracts/ for examples.
   4. If none of the above turn up something solid, see Pillar 4 (Bounded).
   Never answer from your own training. Always cite a file in knowledge/.
   ```

4. Claude Code's built-in `Read` and `Grep` tools handle steps 1-3 with no extra setup. For semantic search across hundreds of docs, add an MCP server (link in repo).
5. Test: ask a question whose answer is in the CSV. The agent should pull and cite the row.

**Takeaway:** An agent that cites *your* materials is an agent you can defend to a partner or a GC. Everything in this pillar is just files in a folder + one rule block in `CLAUDE.md`.

---

## 0:33–0:40 — Pillar 4: Bounded — Escalate When Outside

> If it's not in your knowledge base, it's not the agent's job to answer.

The whole pillar is one rule: **the KB is the fence.** If retrieval comes up empty or low-confidence, the agent doesn't guess — it escalates.

For Mona: the agent answers playbook questions and triages contracts. The moment something needs an actual legal judgment call — *should we walk from this deal?* — it routes to her or to outside counsel with full context attached. That handoff is the *premium* feature, not a failure.

**Demo:** Ask something genuinely out of scope — *"Can you draft me a termination notice?"* The agent declines, explains why, and escalates with a clean summary.

### DIY: Set This Up in Claude Code

1. Add this to **`CLAUDE.md`**:

   ```markdown
   # The Fence — Escalate When You're Outside It
   If you cannot find a clear answer in knowledge/, you MUST NOT guess.
   Instead, reply with exactly this format:

     ESCALATE
     Question: <restate the user's question>
     What I checked: <files you read>
     Why I couldn't answer: <one sentence>
     Suggested next step: <e.g., "ask Mona", "engage outside counsel">

   Out-of-scope examples that must escalate:
   - Drafting new contract language (vs. reviewing existing)
   - Strategic "should we do this deal" questions
   - Anything involving litigation, employment law, or IP filing
   ```

2. Test: ask *"Can you draft me a termination notice?"* — it should return the ESCALATE block, not a draft.
3. **Optional automation:** add a hook in `.claude/settings.json` that watches for the `ESCALATE` keyword and pings Slack/email. (Recipe in the repo — skip live unless someone asks.)

**Takeaway:** "I don't know — let me get the expert" is what makes the tool trustworthy. One rule block in `CLAUDE.md` and you're done.

---

## 0:40–0:45 — Wrap + Q&A

Walk the diagram one last time. Four boxes, four guardrails:

1. **Context** — ask before you answer (one `CLAUDE.md` block)
2. **Memory** — remember and flag (two markdown files + a rule)
3. **KB-First** — answer from sources (a `knowledge/` folder + a rule)
4. **Bounded** — escalate when outside (one rule + one escalation format)

Closing line:

> *Every "AI is unreliable" story you've heard is a story about one of these four guardrails being missing. Put them in, and you have a tool you can hand to your team tomorrow. Everything we did today is in the repo on the screen — clone it, adapt the markdown, and you've got your own.*

Share the GitHub repo link. Open Q&A.

---

## What's in the Take-Home Repo

Spell this out on the last slide so attendees know what they're getting:

- This lesson plan as a markdown doc
- A starter `CLAUDE.md` for a contract-review agent (edit for your domain)
- Sample `memory/red-flags.md` and `memory/green-flags.md`
- A starter `knowledge/clause-matrix.csv` with 10 rows to adapt
- 2–3 sample playbook docs (anonymized)
- A short `SETUP.md` with the Claude Code install + login steps
- An `ESCALATE-HOOK.md` recipe for piping escalations to Slack (optional)

---

## Pre-Flight (instructor)

- Laptop with Claude Code installed + logged in, terminal font bumped to 18pt+.
- Two browser tabs pre-loaded: gemini.google.com, chat.openai.com.
- The indemnity-cap question copy-pasteable from a sticky note (don't fumble it live).
- Diagram open on a second monitor or backup tab.
- Seed `knowledge/` folder pre-staged with the clause matrix, 2–3 playbook docs, and a couple of sample contract paragraphs.
- A short pre-baked NDA paragraph containing a red-flag phrase ("unlimited liability") ready to paste for the Pillar 2 demo.
- GitHub repo public + URL on a sticky note for the wrap.

## Pre-Flight (attendees who want to follow along)

Mention at the start: *"You don't need to follow along live — the repo has everything. But if you want to, install Claude Code now (link in chat) and you'll be able to copy what I do."*
