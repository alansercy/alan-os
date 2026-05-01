# VIE Pattern Extraction — Top 10 Implementation Queue
**Date:** 2026-05-01
**Source:** VIE Groups 1-7 v2 three-lens re-evaluation (33 URLs)
**Canonical Location:** `C:\Veritas\repos\alan-os\memory-bank\VIE_PATTERN_ACTION_LIST.md`
**Owner:** Alan Sercy / Veritas AI Partners

These are the patterns the original single-lens rubric missed.
Each one is actionable. Ordered by impact + effort ratio.

---

## Pattern 1 — Model Tier Routing
**Source:** `8BZupIIVhjs` (3 tricks to reduce token usage)
**Effort:** Low | **Priority:** Immediate
**Stack layer:** Intelligence / Orchestration

**What it is:**
Route tasks to the right model tier by complexity:
- **Opus** → planning, architecture decisions, complex reasoning
- **Sonnet** → execution, code generation, standard tasks
- **Haiku** → classification, triage, simple lookups

**Current state:** Everything runs Sonnet by default. No routing logic.

**Implementation:**
In `orchestrator.py` and `yt_transcribe.py`, add a `model_tier` parameter:
```python
MODEL_TIERS = {
    "plan": "claude-opus-4-20250514",
    "execute": "claude-sonnet-4-20250514",
    "classify": "claude-haiku-4-5-20251001"
}
```
- VIE evaluation prompt → Sonnet (current, correct)
- Orchestrator decompose step → Opus
- Triage classification (Lux inbox) → Haiku
- Session-log summarization → Haiku

**Expected impact:** 30-50% token cost reduction on orchestrator runs.

---

## Pattern 2 — Three-Stage GSD Protocol
**Source:** `xM99M7aLFhQ` (plugin that fixed Claude Code workflow)
**Effort:** Low | **Priority:** Immediate
**Stack layer:** Orchestration / Memory

**What it is:**
Every Claude Code session follows three explicit stages:
1. **Discovery** — read all context, report state, identify gaps
2. **Phase Planning** — decompose work into discrete phases, get approval
3. **Phase Execution** — execute one phase at a time, confirm before next

**Current state:** Sessions do discovery but planning and execution phases blur together. Claude Code sometimes builds across multiple concerns in one shot.

**Implementation:**
Add to `CLAUDE.md` §1 Session Protocol:
```
MANDATORY SESSION STAGES:
1. DISCOVERY — read CLAUDE.md, PROJECTS.md, session-log.md. 
   Report state. Identify blockers. Stop.
2. PLANNING — decompose work into phases. Present to Alan. 
   Get explicit approval before proceeding.
3. EXECUTION — one phase at a time. Confirm completion 
   before starting next phase.
Never skip from Discovery directly to Execution.
```

**Expected impact:** Fewer mid-session course corrections, cleaner commits.

---

## Pattern 3 — Slash Command Shortcuts as Interface Layer
**Source:** `M9lAIBQerUI` (Claude into marketing department)
**Effort:** Medium | **Priority:** Next session
**Stack layer:** Interface / Orchestration

**What it is:**
Define a library of slash commands that map to complex multi-step workflows. User types `/post` or `/digest` or `/prospect` — orchestrator knows exactly what to run.

**Current state:** You type natural language directives. Orchestrator interprets them. Inconsistent.

**Implementation:**
Create `COMMANDS.md` in repo root:
```
/digest — run daily_digest_v3.py
/triage — run lux_launcher.py
/prospect <company> — run MMM prospect research workflow
/vie <url> — run yt_transcribe.py on single URL
/task <title> — add task to tasks.json via /tasks endpoint
/handoff — run push_handoff.py
```
Wire into `orchestrator.py` as first-pass regex before natural language decomposition. Slash commands bypass LLM interpretation — direct function calls. Faster, cheaper, deterministic.

**Expected impact:** Eliminates ambiguity on common operations, reduces orchestrator token cost.

---

## Pattern 4 — End-of-Session Structured Write Protocol
**Source:** `2bvuLxj6nT4` (How to build a Second Brain)
**Effort:** Low | **Priority:** Immediate
**Stack layer:** Memory

**What it is:**
Every session closes with a structured write to a defined vault pointer — not just session-log.md but a specific, queryable record of what was learned, decided, and built.

**Current state:** `push_handoff.py` writes to Drive. Session-log.md gets an entry. But decisions and learnings aren't structured — they're narrative.

**Implementation:**
Add to `push_handoff.py` a structured decisions block:
```json
{
  "session_date": "2026-05-01",
  "decisions": [
    {"decision": "VIE rubric expanded to three lenses", "rationale": "original missed 67% of value"},
    {"decision": "saved→adopted enum rename", "rationale": "align with STACK_DESIGN.md language"}
  ],
  "patterns_adopted": ["model tier routing", "three-stage GSD protocol"],
  "open_items": ["SDK cache field mismatch", "tasks.json cleanup"]
}
```
Append to `~/.lux/Data/session_decisions.json`. Dashboard can surface recent decisions. NotebookLM can consume for personal learning.

**Expected impact:** Queryable decision history. Never re-litigate the same decision twice.

---

## Pattern 5 — Skill Packs as Modular Capability Bundles
**Source:** `yaBDLroG0Lo` (Claude Code Agentic OS)
**Effort:** Medium | **Priority:** Next session
**Stack layer:** Intelligence / Memory

**What it is:**
Group related skills into named packs that load together. Instead of individual skill files, you have `research_pack`, `content_pack`, `bd_pack` — each containing 5-8 related skills that work together.

**Current state:** 65 skills installed globally via GSD. Flat structure. No grouping by use case.

**Implementation:**
Audit `~/.claude/skills/` and group into packs:
- `stack_pack` — VIE evaluation, architecture decisions, principles review
- `content_pack` — Loretta brand, social posts, email drafts
- `bd_pack` — MMM prospecting, lead enrichment, outreach sequences
- `ops_pack` — triage, digest, handoff, task management

Each pack gets a `_pack_loader.md` that references its members. CLAUDE.md references pack by name not individual skills. Modular — swap a pack without touching others.

**Expected impact:** Cleaner CLAUDE.md, faster context loading, easier to hand to AgentOS clients.

---

## Pattern 6 — Markdown-as-Orchestration + Folders-ARE-the-Architecture
**Source:** `337Qc9vOxwY` (Build something that lasts)
**Effort:** Low | **Priority:** Immediate
**Stack layer:** Orchestration / Memory

**What it is:**
The folder structure IS the system architecture. Every folder name is a contract. CLAUDE.md is the routing layer — it tells Claude what each folder contains and when to use it. No separate documentation needed.

**Current state:** Folder structure is mostly right but CLAUDE.md doesn't explicitly describe what each folder IS and when Claude should read from it.

**Implementation:**
Add to `CLAUDE.md` §1 a folder contract section:
```
FOLDER CONTRACTS:
- workflows/        → production scripts, never edit without tests
- memory-bank/      → session state, always read on open
- orchestrator/     → agent specs, read before spawning agents
- agents/           → active agent task files, ephemeral
- sops/             → process definitions, reference only
- templates/        → reusable output templates
- docs/             → company narrative, product specs, reference
```
**Expected impact:** Claude Code navigates the repo correctly without asking. Reduces session setup time.

---

## Pattern 7 — Build-Log-as-Marketing
**Source:** `UfYP7t903Pc` (Stop Building, Start Posting)
**Effort:** Low | **Priority:** Next session
**Stack layer:** Signal / GTM

**What it is:**
Every significant build decision, architecture choice, or shipped feature is a LinkedIn post. The build log IS the content calendar. You're already doing the work — the post is a 5-minute extraction.

**Current state:** Building in private. LinkedIn Authority Track is queued but not running.

**Implementation:**
Add to session-close checklist (CLAUDE.md §4):
```
5. LinkedIn post candidate — did anything ship today 
   worth a 3-sentence post? If yes, draft it and 
   add to content queue.
```
Wire to Loretta's content calendar Google Sheet as a second tab — "Veritas Build Log" — one row per session with post-worthy items flagged. Content engine picks them up.

**Expected impact:** LinkedIn Authority Track starts running automatically from build activity. Zero extra effort.

---

## Pattern 8 — OODA and Scaffold Prompt Prefixes
**Source:** `-CO3ohQqloA` (5 Secret Claude Hacks)
**Effort:** Low | **Priority:** Immediate
**Stack layer:** Intelligence

**What it is:**
Prefix prompts with decision-framework triggers that activate specific reasoning modes:
- `OODA:` → Observe, Orient, Decide, Act (military decision framework — good for competitive analysis)
- `SCAFFOLD:` → builds from first principles up (good for architecture design)
- `STEELMAN:` → find the strongest version of an opposing argument
- `PRE-MORTEM:` → assume failure, work backwards to find why

**Current state:** Prompts are ad hoc. No systematic framework activation.

**Implementation:**
Add to `CLAUDE.md` §7 Gotchas a prompt prefix library:
```
PROMPT PREFIX LIBRARY:
- OODA: — competitive/market analysis
- SCAFFOLD: — architecture and system design  
- STEELMAN: — evaluating tools or approaches critically
- PRE-MORTEM: — risk assessment before building
- EXTRACT: — pull patterns from content (VIE use case)
```
Document in skill files for consistent use across sessions.

**Expected impact:** More structured reasoning on complex decisions. Especially useful for VIE evaluation and architecture choices.

---

## Pattern 9 — Public Skill Repo as Marketing + Versioned Skill Convention
**Source:** `AQ_ca27ftQs` (Claude Made Marketing Agencies Irrelevant)
**Effort:** Medium | **Priority:** Backlog
**Stack layer:** Signal / GTM / Memory

**What it is:**
Maintain a public GitHub repo of Veritas skill files — sanitized versions of what's running in production. Each skill is versioned (`skill_v1.md`, `skill_v2.md`). The repo IS the proof of work and the lead generation mechanism for AgentOS.

**Current state:** Skills are private, global, flat. No versioning. No public presence.

**Implementation:**
- Create `veritas-public-skills` GitHub repo
- Publish sanitized versions of top 10 production skills
- Version each skill file
- README explains Veritas OS methodology
- Links to AgentOS waitlist

**Expected impact:** Proof of work for BD conversations. AgentOS lead generation. Forces discipline on skill quality.

---

## Pattern 10 — Skill-File Ordering for Token Efficiency
**Source:** `LXB_dBvDSOE` (Redesign Claude Design?)
**Effort:** Low | **Priority:** Immediate  
**Stack layer:** Intelligence / Memory

**What it is:**
The ORDER of content in skill files and CLAUDE.md affects token efficiency. Put the most-frequently-referenced content at the top of the file — Claude reads top-down and stops when context window fills. Critical rules at top, examples at bottom.

**Current state:** CLAUDE.md and skill files are ordered by when things were added, not by access frequency.

**Implementation:**
Reorder `CLAUDE.md` sections by frequency of reference:
1. Session Protocol (every session)
2. Technical Rules (every build session)
3. Gotchas (every session — recently added, correct position)
4. Folder Contracts (every session)
5. Skill Convention (build sessions)
6. Project context (as needed)
7. Long-form reference (rarely needed)

Same principle applied to each skill file — critical path first, edge cases last.

**Expected impact:** Meaningful token reduction on long sessions where CLAUDE.md is re-read multiple times.

---

## Implementation Session Queue

### Session A — Immediate (1-2 hours, low effort patterns)
Patterns 1, 2, 4, 6, 8, 10 — all CLAUDE.md and config changes, no new code.

```
Read CLAUDE.md, PROJECTS.md, memory-bank/session-log.md.
Read memory-bank/VIE_PATTERN_ACTION_LIST.md.

MANDATORY FIRST STEP — Pre-build audit before touching 
anything. Principle 7: Build Only What Doesn't Exist.

Run this audit and report findings:

1. List ~/.claude/ contents — any installed tools, 
   superpowers, plugins, or extensions beyond GSD skills
   
2. List ~/.claude/skills/ — do any GSD skills already 
   cover model tier routing, prompt prefixes, session 
   protocol, folder conventions, or slash commands?
   Read the relevant skill files if names suggest overlap.

3. Check orchestrator.py — does it already have model 
   tier selection or routing logic?

4. Check CLAUDE.md in full — what sections already exist?
   Flag any overlap with the 6 Session A patterns:
   - Session protocol stages (Discovery/Planning/Execution)
   - Folder contracts
   - Prompt prefix library
   - Model tier routing references

5. Check ~/.lux/workflows/ for:
   - Any slash command handler
   - session_decisions.json writer
   - Skill pack loader

Report what EXISTS. Flag any pattern already partially 
or fully built. Only implement what genuinely doesn't exist.
STOP and confirm findings before implementing anything.

Only after audit confirmed — implement in order:

1. Pattern 1 — MODEL_TIERS dict in orchestrator.py 
   and yt_transcribe.py. Route classify tasks to Haiku.
   SKIP if model routing already exists.

2. Pattern 2 — THREE-STAGE SESSION PROTOCOL in CLAUDE.md §1.
   Discovery → Planning → Execution. Mandatory, no skipping.
   SKIP if already in CLAUDE.md.

3. Pattern 4 — Structured decisions block in push_handoff.py.
   Append to session_decisions.json after each run.

4. Pattern 6 — FOLDER CONTRACTS section in CLAUDE.md.
   SKIP if already documented.

5. Pattern 8 — PROMPT PREFIX LIBRARY in CLAUDE.md §7 Gotchas.
   SKIP if already present.

6. Pattern 10 — Reorder CLAUDE.md sections by access 
   frequency. Critical path first.

One commit per pattern. Report hash after each.
```

### Session B — Next Session (2-3 hours, medium effort)
Patterns 3, 5, 7 — new files, new conventions, content pipeline wiring.

### Session C — Backlog
Pattern 9 — public skills repo. Do after first AgentOS client conversation.

---

## Running ADOPT Count After v2 Re-evaluation

| Pattern | Status | Session |
|---|---|---|
| Folder-as-skill convention | ✅ Implemented (053b256) | Today |
| Gotchas section in CLAUDE.md | ✅ Implemented (053b256) | Today |
| Model tier routing | ⏳ Queued | Session A |
| Three-stage GSD protocol | ⏳ Queued | Session A |
| End-of-session structured write | ⏳ Queued | Session A |
| Folders-ARE-the-architecture | ⏳ Queued | Session A |
| OODA + scaffold prompt prefixes | ⏳ Queued | Session A |
| Skill-file ordering for tokens | ⏳ Queued | Session A |
| Slash command shortcuts | ⏳ Queued | Session B |
| Skill packs as modular bundles | ⏳ Queued | Session B |
| Build-log-as-marketing | ⏳ Queued | Session B |
| Public skill repo | ⏳ Backlog | Session C |
