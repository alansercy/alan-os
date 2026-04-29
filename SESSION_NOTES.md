# SESSION_NOTES — 2026-04-29

**Session focus:** Scope VIE Workflow 5.1 — audit existing components, draft spec, commit.

## What changed

- `docs/workflow_5_1_spec.md` — rewrote (commit `af7b40d`, +204 / −133). Replaced the prior parallel-session draft (`1747450`) with a version anchored on `nlm_feed_builder.py` v1.4 (the live engine), capital-D `.lux\Data\ai_stack_feed.json` storage, per-URL schema, and explicit V2 deferral of n8n.

No other files in this repo touched.

## Decisions made (don't relitigate)

- **Engine for VIE V1 = `nlm_feed_builder.py` v1.4** (not the legacy `ai_research_monitor.py` / `ai_research_backfill.py` pair). Rationale: nlm_feed_builder already does multi-folder reads, three-prompt scoring, Safelink unwrap, dedup registry, and 5 NotebookLM sinks — ~80% of V1 was already shipped.
- **Storage path: `C:\Users\aserc\.lux\Data\ai_stack_feed.json`** (capital D, matches sibling `nlm_processed_ids.json` and `pending_jobs.json`).
- **Schema: per-URL, not per-email.** One email with three URLs becomes three items, each with its own `relevance_score` and `fit_pipeline`. The dashboard ranks links, not emails.
- **n8n deferred to V2.** V2 = multi-source fan-in (GitHub/RSS/X/Reddit) onto the same `POST /ai_stack` sink, at which point lifting orchestration into n8n earns its keep.
- **Existing AlanSercy MSN Flow violates CLAUDE.md §2** (uses `@n8n/n8n-nodes-langchain.anthropic` built-in node). Logged but not fixed this session; only matters if a future session forks MSN Flow.

## Open threads

- **Steps 1–2 of the spec are being built in a parallel Claude Code session** (per Alan, mid-session): `/ai_stack` endpoints in `alan_os_server.py` + `ai_stack_feed.json` skeleton. Smoke test was in progress when this session closed. Confirm landing in the lux-os repo before resuming.
- **Branch is 1 commit ahead of `origin/main`** (`af7b40d`). Not pushed.
- **n8n MCP child still spawned with a stale API key** — `mcp__n8n-mcp__*` returns AUTHENTICATION_ERROR. Direct REST works fine via the key in `C:\Users\aserc\.lux\.env`. The User-scope env and `C:\Veritas\repos\alan-os\.env` both also returned 401 against the live host; `.lux\.env` is the authoritative source. Worth a session-start audit next time before any n8n write.

## Next action

After the parallel session lands Steps 1–2: end-to-end smoke test by running `nlm_feed_builder.py` against a known AI-research email and confirm one item per URL appears in `ai_stack_feed.json` via `GET /ai_stack`.

## Blockers

- None for VIE 5.1 V1. Spec is unblocked, parallel session is implementing.
- Carry-forward from 04-29 (unchanged this session): elevated `schtasks` for AlanOS_Server patch; Anthropic admin API key creation; 3.2 active toggle decision; 2.4 prerequisite env vars on n8n VM.
