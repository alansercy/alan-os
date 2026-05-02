# claude-mem Pilot Notes
**Date:** 2026-05-02 (Session D)
**Task:** task-020 — evaluate claude-mem for alan-os
**Verdict:** REJECT

---

## What It Is

claude-mem (`thedotmack/claude-mem`, npm `claude-mem`) is a Claude Code plugin that
captures session context via lifecycle hooks, compresses it with Claude's agent SDK,
and injects relevant history into future sessions. Persistence layer: SQLite + Chroma
vector search at `~/.claude-mem/`. Background worker service on port 37777. Web UI
included. Latest: v12.4.9 (2026-04-30). License: AGPL-3.0. Stars: ~71K.

---

## Why Install Step Was Skipped

`npx claude-mem install` registers 5 lifecycle hooks (SessionStart, UserPromptSubmit,
PostToolUse, Summary, SessionEnd) into Claude Code's global settings — not into a
project directory. There is no isolated install path: the hooks are system-wide.
Running it in a temp directory only isolates the npm package files, not the hook
registration. Installing would have modified the global Claude Code harness mid-session.
Skipped per "do not modify any existing files" constraint.

---

## Conflict Analysis

### 1. CLAUDE.md auto-generation — CRITICAL conflict

claude-mem auto-generates folder-level CLAUDE.md files during sessions.
`CLAUDE_MEM_FOLDER_CLAUDEMD_ENABLED` is supposed to control this, but the setting
is not respected (upstream Issue #767 — open, unfixed as of v12.4.9). Our
`CLAUDE.md` is version-controlled, carefully structured, and is the single source
of session truth. A plugin that writes to CLAUDE.md regardless of config is
incompatible without a confirmed fix. Cannot safely run alongside our pattern.

### 2. Windows pipe mode — HARD BLOCKER on this platform

`claude --print` returns empty output silently when claude-mem is active on Windows
(upstream Issue #1482 — open, unfixed). This machine is Windows 11. Any automation
or future orchestration that calls `claude --print` would silently no-op. The host
`:5678` listener and future ORCH-3 agent handoffs both depend on reliable subprocess
invocation. This bug alone is a hard reject on Windows.

### 3. Session-close duplication

claude-mem's SessionEnd hook captures and compresses session context automatically.
We already have `push_handoff.py` (Drive write) + `closed_items.md` append +
`session_decisions.json` (P4 pattern, commit `5025baa`). Two parallel session-close
mechanisms with different storage formats (SQLite vs flat files) and no sync would
create drift and confusion about which record is authoritative.

### 4. memory-bank/ duplication

Our memory-bank/ is flat-file, git-tracked, and human-readable — readable in any
text editor, diffable, portable. claude-mem stores to SQLite + Chroma vector search.
No bridge between the two. Running both means maintaining two memory systems with
no clear handoff between them.

### 5. AGPL-3.0 license

Not a blocker for use as-is, but any modifications to claude-mem itself must be
open-sourced. Relevant if we ever need to patch the CLAUDE.md generation bug locally.

### 6. Background service on port 37777

Adds another persistent host service to manage. Low concern relative to the above,
but worth noting: port 37777 joins :8000 (alan_os_server) and :8081 (Lux Command
Center) on the host.

---

## Comparison to Existing Stack

| Capability | claude-mem | Current alan-os |
|---|---|---|
| Session continuity | SQLite + vector search | CLAUDE.md + session-log.md |
| Session close | SessionEnd hook (auto) | push_handoff.py (explicit) |
| Cross-session memory | ~/.claude-mem/ DB | memory-bank/ flat files |
| CLAUDE.md writes | Uncontrolled (bug #767) | Version-controlled |
| Windows support | Broken pipe mode (#1482) | Native |

---

## Recommendation

**REJECT** — same verdict as Ruflo (2026-05-02 pre-install scan).

Primary blockers:
1. Windows pipe mode bug (Issue #1482) — hard blocker on this platform
2. CLAUDE.md auto-generation cannot be disabled (Issue #767) — direct conflict
   with version-controlled CLAUDE.md

Secondary: session-close duplication with push_handoff.py / P4 pattern.

**Re-evaluation gates:**
- Issue #1482 (Windows pipe mode) closed with confirmed fix → re-run pilot
- Issue #767 (CLAUDE.md generation disabled by config) closed → re-run pilot
- Do not re-evaluate until both are resolved

**Do not replace push_handoff.py.** The existing session-close pattern (P4,
`5025baa`) is the authoritative session record. claude-mem would duplicate and
potentially conflict with it.

---

## Install Convention Note

If a future evaluation passes, follow the Ruflo pre-flight rubric before installing:
1. Does it implement capabilities we already have? (routing, memory, session hooks)
2. Does it touch CLAUDE.md? What does the init wizard do — overwrite or merge?
3. Does it conflict with memory-bank/? Which system is authoritative?
4. Does it register global hooks that can't be scoped to a single project?

Any HIGH-overlap or CRITICAL finding → REJECT, document re-evaluation gates.
