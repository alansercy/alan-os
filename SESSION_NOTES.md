# SESSION_NOTES — 2026-04-29 (close)

**Session focus:** Claude Usage card — false start on the orphan port-8000 dashboard, then correctly built as an estimated-usage panel + persistence on the active Lux Command Center (port 8081).

## What changed (this session)

**lux-os (commits):**
- `53b60f3` — feat: Claude usage dashboard card (port-8000 React dashboard, `Dashboard/index.html` + `workflows/daily_burn_rate.py` cost computation). **Now orphan code** — landed on the wrong dashboard before Alan corrected me.
- `3941978` — feat: estimated local usage panel for Lux Command Center (`claude_usage_dashboard.html` panel + `workflows/daily_burn_rate.py` snapshot persistence to `~/.lux/Data/claude_burn_history.json`).
- (parallel session) `952862e`, `eb97800`, `3ef9724` — VIE `/ai_stack` endpoints, AI research script Doc-ID fix, SalesOS dashboard tab. Mine + parallel-session work do not overlap.

**alan-os (commits):**
- `37f7993` — feat: SalesOS dashboard spec V1 + memory-bank entry. **Bundled my "Lux Command Center — Estimated Usage Panel + Burn-Rate Persistence" memory-bank append** alongside the parallel session's spec/memory-bank work in a single commit.
- (parallel session) `1f431c9`, `f6e1f56`, `af7b40d`, `1747450` — VIE 5.1 spec rewrites + closeout entries.

**This close** — `SESSION_NOTES.md` rewrite + `PROJECTS.md` updates (3 lines: dashboard row reflects estimated panel shipped, panel row split into estimated-live vs authoritative-blocked, admin-key blocker scoped to authoritative path only). **Uncommitted at session close** — see Open threads below.

## Decisions made (don't relitigate)

- **Estimated cost stays in `daily_burn_rate.py`** with hardcoded per-model-family rates (Opus 4.x / Sonnet 4.x / Haiku 4.x / 3.5 fallbacks). Flagged "est" in the UI. Authoritative numbers wait on the admin API key.
- **Persistence lives in `daily_burn_rate.py`, not a separate service.** `_record_snapshot()` writes a 15-key lean record per `get_burn_rate()` cache miss. Throttled to 5 min between writes (independent of the 30s data cache). Atomic via `.json.tmp` + `os.replace`. Persistence errors swallowed so `/health` cannot break.
- **History exposed via `/health.claude_burn.history`** rather than a new `/local_burn` endpoint — single endpoint, single cache, dashboard JS already cross-fetches `localhost:8000`.
- **Estimated panel coexists with the (still-empty) admin-API panel** on Lux Command Center. When admin key lands, both render side-by-side and act as a drift check.
- **Orphan commit `53b60f3` left in place.** Doesn't break anything; minimal cost to keep until/unless port-8000 dashboard is intentionally retired.

## Open threads

- **Uncommitted at close:** `SESSION_NOTES.md` (this file, rewrite) + `PROJECTS.md` (3 factual updates, lines 229 / 233-now-234 / authoritative-key paragraph). Asking before commit per close template.
- **Trend sparkline cold-start:** first snapshot persists on first `/health` call after server restart; informative shape needs ~few hours of accumulation. Empty-state copy already covers <1 snapshot.
- **Orphan port-8000 card** (`53b60f3`) — invisible unless that dashboard is opened. Carry-forward decision: revert vs leave.
- **n8n REST 401** carry-forward from the parallel VIE session (User-scope env, `~/.lux/.env`, alan-os `.env` — all rejected). Not blocking VIE V1 (Python-only).
- **AlanOS_Server task patch** still needs elevated `schtasks /Create /F` against `~/.lux/workflows/AlanOS_Server.xml.patched`. Carry-forward from prior sessions.
- **Test data left in place from parallel SalesOS session:** `~/.lux/Data/leads.json` has 4 records, `competitors.json` has 2. For visual verification when Alan loads the dashboard.

## Next action

**Alan:** load `localhost:8081`, scroll to "Estimated Local Usage" panel, confirm it renders the way the screenshot-from-disk verification suggests (4 tiles + sparkline + footer with snapshot count). Ping back if anything is broken.

## Blockers

- **Anthropic admin-scope API key** — manual mint required (Org Admin only, console.anthropic.com). Single blocker on authoritative panel; estimated panel ships without it. Process documented in PROJECTS.md lines 247-259.
- **Elevated PowerShell** for AlanOS_Server task patch (carry-forward).
- **Plan-ceiling math** still impossible without admin key (drift-check requires authoritative org-wide numbers to compare estimated against).
