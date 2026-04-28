# SESSION_PROTOCOL.md — alan-os

How every working session opens and closes. Two surfaces: **claude.ai** (browser) and **Claude Code** (CLI in this repo). Each has an explicit open and close step. The point is zero context loss between sessions and across surfaces.

---

## Artifact map

| File | Location | Purpose | Lifecycle |
|------|----------|---------|-----------|
| `PROJECTS.md` | repo root | Live status board across all workflows and infra | Updated during work; source of truth |
| `CONTEXT.json` | repo root | Machine-readable system state (clients, workflows, drive registry, rules) | Updated during work; source of truth |
| `SESSION_NOTES.md` | repo root | Most-recent Claude Code session handoff | **Overwritten** each Claude Code close |
| `HANDOFF_YYYY-MM-DD.md` | repo root | Dated handoff from a claude.ai session | **Accumulates** — one per claude.ai session |
| `templates/HANDOFF_TEMPLATE.md` | repo | Blank form Alan fills in to produce a `HANDOFF_<date>.md` | Static template |
| `templates/session_close.md` | repo | Prompt Alan pastes into Claude Code to close a session | Static template |
| `templates/session_start.md` | repo | Prompt Alan pastes into a new claude.ai chat to resume | Static template |

Rule of thumb: **`PROJECTS.md` and `CONTEXT.json` are the durable state. `SESSION_NOTES.md` and `HANDOFF_*.md` are session-to-session glue.**

---

## The four states

### 1. Claude Code — session open

Alan pastes this prompt into a fresh Claude Code session (it's the same prompt that opened this very protocol):

> Read PROJECTS.md and CONTEXT.json. Read SESSION_NOTES.md if it exists. Load your memory of this repo, then tell me: what's the current state, what was last worked on, and what's the next action. Do not start building until I confirm the direction.

Claude Code reads the three files, loads its persistent memory for this repo, summarizes, and waits for direction.

### 2. Claude Code — session close

Alan pastes the contents of `templates/session_close.md` into Claude Code. Claude Code:

1. Reviews what changed this session (`git status`, `git log` since session start, working tree).
2. Writes a fresh `SESSION_NOTES.md` to repo root (overwriting the previous one).
3. Reports the file location and any uncommitted state.

`SESSION_NOTES.md` is the breadcrumb for the **next Claude Code session**. It is intentionally short and operational — not a journal.

### 3. claude.ai — session close

Alan opens `templates/HANDOFF_TEMPLATE.md`, fills it in by hand based on what happened in the claude.ai chat, saves it as `HANDOFF_YYYY-MM-DD.md` in repo root, and commits it. This is the only step in the protocol that is **manual** — claude.ai cannot write to the repo.

If two claude.ai sessions happen in one day, append `-2`, `-3`, etc. (e.g. `HANDOFF_2026-04-28-2.md`).

### 4. claude.ai — session open

Alan pastes the contents of `templates/session_start.md` into a fresh claude.ai chat. The prompt instructs claude.ai to:

1. Fetch the latest `PROJECTS.md` from the GitHub raw URL.
2. Read the `HANDOFF_<date>.md` contents Alan pastes below the prompt.
3. Summarize state and wait for direction.

---

## Setup

Before `session_start.md` works against a real GitHub URL, the repo needs a remote and `<GITHUB_RAW_PROJECTS_URL>` in `templates/session_start.md` needs to be replaced with the actual raw URL — typically:

```
https://raw.githubusercontent.com/<owner>/alan-os/main/PROJECTS.md
```

Until then, paste `PROJECTS.md` contents into the chat alongside the handoff.

---

## Conventions

- **Dates are absolute.** Always `YYYY-MM-DD`, never "yesterday" or "Thursday."
- **`SESSION_NOTES.md` is overwritten, not appended.** History lives in git.
- **`HANDOFF_*.md` files accumulate.** They are the only persistent record of claude.ai sessions, since those chats aren't in the repo.
- **`PROJECTS.md` and `CONTEXT.json` are updated during the session, not at close.** Close steps capture what changed, they don't catch up on stale state.
- **Commit on close.** Every close should end with a commit so the next session starts from a clean tree.
