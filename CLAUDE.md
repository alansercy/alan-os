# Claude Code Context — alan-os

This file is read automatically by Claude Code at session start. It carries the durable context for working in this repo so manual context pasting is no longer required.

---

## 1. Project Identity

**alan-os** is the orchestration repo for the Veritas AI Partners stack — the operating system Alan Sercy uses to run client work, personal infrastructure, and family projects. It holds the master `PROJECTS.md` status board, `CONTEXT.json` machine-readable state, the ORCH-1/ORCH-2 Python orchestrators, the n8n workflow JSON exports, and the session protocol SOP.

**Veritas AI Partners** (CentPenny LLC) is Alan's revenue infrastructure for SMB and PE-backed clients. Product stack: AgentOS, PersonalOS, TradeOS, SalesAgentOS, FinanceOS (backburner), Digital Presence.

**Canonical repo locations** (all under `C:\Veritas\repos\`):
- `C:\Veritas\repos\alan-os` — this repo: orchestrator + workflows + status board
- `C:\Veritas\repos\loretta-os` — Loretta MoveWithClarity n8n workflows
- `C:\Veritas\repos\apexbot` — ApexBot Evony automation (Python)

`C:\Users\aserc\.lux\` is **not** a repo — it stays where it is. It holds the dashboard server, triage scripts, secrets (`.env`), and the Norman Inbox Guard. Never move it.

**Canonical assets** live under `C:\Veritas\assets\` (veritas, loretta, mmm, lovie-and-lollie, apexbot, personal). Archive is at `C:\Veritas\archive\`.

---

## 2. Technical Rules (non-negotiable, never deviate)

These have been earned the hard way. Never deviate without explicit confirmation.

### n8n HTTP Request to Anthropic API
- HTTP Request node `typeVersion 4.2`
- Header: `x-api-key` (not `Authorization`)
- Header: `anthropic-version: 2023-06-01`
- `contentType: raw`
- Body: `={{ $json.apiBody }}`
- **Never use the built-in Anthropic node.** It breaks on edge cases.

### Google Sheets nodes
- `documentId` and `sheetName` always use the `__rl` resource locator wrapper. No raw IDs.

### n8n API PUT requests (workflow updates)
- Strip these fields before PUT: `active`, `createdAt`, `updatedAt`, `versionId`, `tags`, `id`. Sending any of them causes silent failure.

### Email sanitization for Sheets / triage
- Strip `/[\x00-\x1F\x7F-\xFF<>"\\]/g`
- Join lines with `||` not `\n`

### Gmail field names
- Capitalized: `From`, `Subject`. Lowercase variants miss matches.

### n8n endpoint
- Public URL: `https://n8n.lorettasercy.com`
- The host machine cannot reach the VM's `localhost:5678`. Use the public URL or work in the n8n web UI.

### Deploy fallback (when API rejects)
- n8n web UI → browser console (Ctrl+Shift+J) → allow pasting → run script. This is the fallback when the n8n REST API rejects an operation.

---

## 3. Current System State

**Repos:** all under `C:\Veritas\repos\` (see Project Identity).

**Local infrastructure:** `C:\Users\aserc\.lux\` — dashboard, triage, Norman Guard, secrets. **Do NOT move.**

**n8n credentials needing reauth:** none — `sG8kOyb5bJb0hjgS`, `xkF1H9p5Q52UPPoi`, `gbwzaRu0ONWfhuUr` all confirmed green in n8n UI on 2026-04-29.

**Active / live workflows (n8n IDs):**
- **3.1** `r1pkTZ94DuuWrTtA` — MMM Gmail Triage
- **3.2** `VvHYTjheeecJ441F` — MMM Prospect Audit
- **2.1**, **2.2** — Loretta content (OAuth blocked)
- **2.4** `tX09Uxf9LdjVLmvl` — Loretta video repurposing (deployed + active 2026-04-29)

**Alan OS Dashboard:** `localhost:8000/dashboard` — server at `C:\Users\aserc\.lux\workflows\alan_os_server.py`.

---

## 4. Session Protocol

### Mandatory Session Stages

Every session follows three explicit stages. Never skip from Discovery directly to Execution.

1. **DISCOVERY** — read `CLAUDE.md`, `PROJECTS.md`, `memory-bank/session-log.md`. Report current state. Identify blockers. Stop and present findings.
2. **PLANNING** — decompose work into discrete phases. Present the plan to Alan. Get explicit approval before proceeding.
3. **EXECUTION** — one phase at a time. Confirm completion before starting the next phase.

See `SESSION_PROTOCOL.md` for the full canonical protocol. Always:

- **Memory bank reads precede all skill invocations.**
- Read `PROJECTS.md` first.
- Read `SESSION_NOTES.md` if it exists (most recent breadcrumb).
- Report current state before building anything.
- Write `SESSION_NOTES.md` on session close (use `templates/session_close.md`).
- **Never delete files without a confirmed copy elsewhere.**
- **Ask before any action that touches credentials or `C:\Users\aserc\.lux\`.**

### Session-close checklist (mandatory before declaring session over)

The dashboard treats `~/.lux/Data/tasks.json` and `~/.lux/Data/projects.json` as
the single source of truth — the digest now reads from these files (lux-os
commit `0d14134`), and the dashboard Tasks tab now writes back via the
in-tab task form (POST `/tasks`). Closing a session without updating these
files leaves both surfaces stale.

Every session before closing must:

1. **Mark completed tasks `done` in `tasks.json`** — anything actually finished
   this session. Either via the dashboard's Complete button (PATCH `/tasks/{id}`
   sets `status="done"` + stamps `completed_at`) or by direct JSON edit if the
   server isn't running. Do not let "done in conversation" leave open rows
   behind.
2. **Add any new tasks surfaced during the session** to `tasks.json` — via the
   dashboard's New Task form (preferred) or direct edit. Capture the work
   before context is lost. New `id` is `task-{N:03d}` where `N = len(tasks)+1`.
3. **Update affected `projects.json` status fields** — `status` (`green` /
   `yellow` / `red` / `idle`) and `status_note` should reflect reality at
   close. The digest renders these directly into the morning email.
4. **Confirm `push_handoff.py` fired** — at `C:\Users\aserc\.lux\workflows\`.
   Pushes the handoff doc to Drive (asset `1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ`
   per `PROJECTS.md` Drive Asset Registry). Without this, claude.ai and Claude
   Code sessions cannot resume from the same breadcrumb.
5. **LinkedIn post candidate** — did anything ship today worth a 3-sentence
   post? If yes, draft it and append to the Veritas Build Log tab on the
   Loretta Content Calendar (sheet `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`).
   Run: `python scripts/build_log.py append --repo <repo> --head <hash>
   --shipped "<1-2 sentences>" --post-candidate Y --draft "<3-sentence post>"
   --status draft`. If nothing post-worthy shipped, skip — do not append a no-op
   row. Pattern 7 from `memory-bank/VIE_PATTERN_ACTION_LIST.md` — the build log
   IS the LinkedIn content calendar; zero extra effort beyond the draft itself.

If `:8000` (alan_os_server) is up, the dashboard `Tasks` tab is the fastest
path for #1 and #2. If it's down, read/write `tasks.json` directly with the
same shape backend `POST /tasks` produces.

---

## 5. Active Projects (top 5)

Pulled from `PROJECTS.md` Session Queue + TIER 1. Read `PROJECTS.md` for full context.

1. **MMM-fix** — Re-auth Gmail cred `68RydHz0N1dUAj9S` in n8n UI; run `handoff/vm-scripts/01` + `02` in elevated PS on VM; click Execute on workflow `VvHYTjheeecJ441F` to verify 3.2.
2. **Workflow 2.4 deploy** — Re-auth the three Google creds; set `OPUS_CLIP_API_KEY` / `BUFFER_ACCESS_TOKEN` / `BUFFER_PROFILE_IDS`; create `Video Log` Sheet tab; import `workflows/workflow_2_4_video_repurposing.json`; activate.
3. **Workflow 2.3 finish** — After Twilio account exists: store credential, fill `__SET_*__` placeholders in `AukTldfaY4oWcu1Q`, activate.
4. **ApexBot Session 3** — `events.yaml` SVS/KE flags, template capture (gather/march/close-popup), scheduler wiring for 4 alts.
5. **Loretta L1** — Wire Buffer auto-post (Telegram intake C is live); then `/relist-guide` page next session.

---

## 6. Context Window Discipline

- Stay under **100K tokens**. Warn Alan if approaching the limit.
- Use `/clear` when context is heavy — files are saved to disk, not memory.
- **Never hold full file contents in memory** when a path reference works. Cite file paths instead of pasting.

---

## 7. Gotchas (negative-example log)

Lessons earned through session failures and Alan-corrections. Distinct from §2 ("non-negotiable rules") — these are the *stories* behind the rules and the gotchas that don't reduce cleanly to a one-liner. Seed-and-grow list; append on every new lesson.

1. **n8n PUT — strip metadata fields before sending.** Sending `active`, `createdAt`, `updatedAt`, `versionId`, `tags`, or `id` to `PUT /api/v1/workflows/{id}` causes the API to *silently* accept the request with HTTP 200 but reject the actual update. The workflow appears unchanged. Always strip these six fields before PUT. (See §2 for the canonical rule.)

2. **n8n Anthropic — never use the built-in node.** The HTTP Request node at `typeVersion 4.2` with `x-api-key` header, `anthropic-version: 2023-06-01`, `contentType: raw`, body `={{ $json.apiBody }}` is the only path that survives edge cases (long prompts, tool use, prompt caching). The built-in Anthropic node breaks on multi-turn or large bodies and gives no useful error. (See §2.)

3. **Google Sheets — `__rl` resource locator wrapper is mandatory.** Both `documentId` and `sheetName` parameters require the resource locator object (`{__rl: true, value, mode: "list", cachedResultName, cachedResultUrl}`), not raw strings. Raw IDs validate but fail at runtime with cryptic "resource not found" errors. (See §2.)

4. **MMM Prospect Tracker — header row is row 3, not row 1.** Banner content occupies rows 1–2. Sheet has 6 tabs; the `(n8n)` tab (19 cols, no Email-1/2/3 sent dates) is the integration target — separate from the human `WA Prospect Tracker` tab so writes don't trample manual edits. The `#` column (col B) is the de-facto lead key since there's no native `Lead ID` column — fragile if rows get inserted mid-table.

5. **Windows bash + curl POST — use heredoc + `--data-binary @file.json`.** Standard `curl -d '{...}'` quoting is mangled by Windows bash even with single quotes, returning HTTP 422. Pattern that works: `cat > /tmp/req.json <<'EOF' ... EOF` then `curl --data-binary @/tmp/req.json`. Applies to any non-trivial JSON POST from this shell.

6. **Headless-Chrome `--dump-dom` on Windows — convert tempfile paths via `cygpath -w`.** Bash `/tmp/...` paths confuse Chrome on Windows; `cygpath -w /tmp/foo.html` returns a Windows-form path Chrome accepts. Required pattern any time you want DOM-after-JS verification from a CLI.

7. **Desktop OAuth flow — `flow.run_local_server(port=0)` is the clean pattern.** For Google Workspace API access from local scripts: `InstalledAppFlow.from_client_secrets_file(...).run_local_server(port=0)` opens one browser pop, no manual code paste, persists refresh token via `to_json()`. Future runs reload silently via `from_authorized_user_file`. Used for `post_closeout_to_drive.py` against the Veritas Session Log Doc. Same pattern works for Sheets, Drive, Calendar with adjusted scopes.

8. **Verify existing code actually does what you think before recommending "extend, don't build new."** Build-or-extend (P7 in `PRINCIPLES_REVIEW_v1.md`) is only honest if the "extend" recommendation rests on verified code behavior, not assumed behavior. VIE session 2026-05-01: I recommended extending `shorts_researcher.py` for transcript work; Alan's verification challenge forced a re-read which proved the file is metadata-only (regex on YouTube page HTML, no yt-dlp, no transcripts anywhere in codebase). Corrected recommendation: build the new transcript layer, integrate via existing `/ai_stack`. Rule: when proposing extend-not-build, cite line numbers and confirm the function does what you're claiming it does — don't infer from filename or one-line summary.

---

## 8. Skill File Convention (folder-as-skill)

When authoring Claude Code skills (system-level, at `C:\Users\aserc\.claude\skills\`), prefer **folder structure** over single-file:

```
my-skill/
  prompt.md          # the canonical instructions Claude reads
  scripts/           # any scripts the skill references
  examples/          # worked examples / negative examples
  templates/         # boilerplate the skill instantiates
```

**Why:** progressive disclosure (Claude reads `prompt.md` first, pulls in `scripts/` or `examples/` only when relevant), single canonical store per skill (no scattered assets), explicit asset coupling (everything the skill needs lives in one folder).

**Scope note:** This repo (`alan-os`) does not host Claude Code skills — those live in `~/.claude/skills/`. Convention documented here so any future skill creation (this repo or a global skill referencing repo assets) follows the pattern. Existing single-file skills referencing external assets should be migrated to folder structure when next touched.

**Source:** STACK_DESIGN.md §2 ADOPT verdict on `youtube.com/shorts/3E59wf8RA8Y` (AI Honeycove, 2026-05-01).

---

## 9. Skill Packs

Skills are grouped by Veritas use case in `docs/skill_packs/`. Load the relevant pack file when starting work in that domain rather than scanning all 100+ available skills.

- **`stack_pack`** — VIE evaluation, AI infrastructure, architecture decisions, systematic debug
- **`content_pack`** — Loretta content engine + Veritas marketing copy + BD outreach (BD uses content_pack with a different lens; the originally-proposed `bd_pack` was a strict subset and was dropped)
- **`ops_pack`** — daily ops loop (triage / digest / handoff / task) + scheduling + harness config

GSD skills (`gsd-*`) and n8n skills (`n8n-*`) stay implicitly grouped by prefix and are not packed — load them by name when needed.

Pattern 5 from `memory-bank/VIE_PATTERN_ACTION_LIST.md`. Pack files are pointer-lists, not relocators — member skills live at `~/.claude/skills/<name>/` unchanged.

---

## MEMORY BANK PROTOCOL
- Before starting any task: read memory-bank/session-log.md
- After completing any task: append a dated summary to memory-bank/session-log.md
- Format: ## [DATE] [TASK NAME]\n- What was done\n- What worked\n- Blockers\n- Next step

## Required context
- docs/veritas-company-narrative.md — load every session for company vision, product portfolio, and exit thesis
