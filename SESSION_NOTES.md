# SESSION_NOTES — 2026-04-29 (close)

**Session focus:** VIE Workflow 5.1 — Steps 1-2 implemented + smoked + pushed.

## What changed (this session)

**lux-os:**
- `eb97800` — fix: `ai_research_monitor.py` + `ai_research_backfill.py` Doc ID switch from `1f3RGBRl...` → canonical `1WD2Sr2H...` (Veritas AI Research Feed)
- `952862e` — feat: `/ai_stack` endpoints in `alan_os_server.py` (4 endpoints, per-URL schema per spec `af7b40d`, validated 0-10 score + enum membership for `fit_pipeline` / `url_category` / `status`)
- `~/.lux/Data/ai_stack_feed.json` — empty skeleton on disk, gitignored

**alan-os:**
- `1747450` — initial spec draft (superseded by parallel session's `af7b40d`); both already pushed
- This commit (memory-bank append + this file) — session close artifacts

## Spec status

`docs/workflow_5_1_spec.md` (commit `af7b40d`) is canonical. Endpoints in `alan_os_server.py` match its schema exactly: per-URL records, nested `source` object, `relevance_score` 0-10, `fit_pipeline` single-string enum, dedup on `url`, `GET /ai_stack/digest` registered before any `/ai_stack/{id}` route.

## Smoke verified (live, 2026-04-29 ~14:11)

7 calls round-tripped clean: POST create + GET list + POST dedup + PATCH status/tags + digest scoping + 400 on bad `fit_pipeline` + 400 on out-of-range `relevance_score`. Server PID 29416 after `/admin/restart` (~63s cold cycle — note Task Scheduler `/Run` is slow; budget the wait).

## Decisions made (don't relitigate)

- **Build sequence Step 1 = backend; Step 2 = nlm_feed_builder augmentation; Step 3 = end-to-end smoke; Step 4 = dashboard tab.** Per build sequence in `af7b40d`. Steps 1 done.
- **JSON skeleton stays empty in version control** — `data/` is gitignored on lux-os, runtime state only.
- **n8n V2 deferral confirmed** — V1 is Python-only; n8n migration earns its keep when V2 multi-source fan-in lands.

## Open threads / blockers

- **n8n REST 401** across User-scope env, `~/.lux/.env`, and `~/Veritas/repos/alan-os/.env`. The 04-29 rotation key (`...ybaE`) is being rejected. Not critical for VIE V1; blocking if n8n V2 work starts. Worth a session-start audit next time.
- **AlanOS_Server task patch unfinished** — patched XML built and verified at `~/.lux/workflows/AlanOS_Server.xml.patched`; non-elevated `schtasks /Create /F` returns "Access is denied". Carry-forward.
- **Carry-forward from 04-29 spec session (unchanged):** Anthropic admin API key creation (PROJECTS.md line 233); 3.2 active toggle decision; 2.4 prerequisite env vars on n8n VM.

## Next session — start here

**Step 2:** augment `~/.lux/workflows/nlm_feed_builder.py`:
1. Add `extract_ai_stack_urls(body) -> list[dict]` (port from `extract_ai_links.py:21-46`, reuse `unwrap_safelink()` already in nlm_feed_builder:104-113)
2. Add `AI_STACK_URL_ENRICH_PROMPT` constant per spec lines 133-157
3. After existing `score_email()`, loop extracted URLs → Claude enrich → `POST http://localhost:8000/ai_stack` per URL
4. Treat POST failures as non-fatal warnings (existing `nlm_processed_ids.json` registry handles overall email dedup)

Then **Step 3** (run nlm_feed_builder against a known AI-research email, verify one item per URL via `GET /ai_stack`, run twice to verify URL-level dedup), then **Step 4** (dashboard tab).

## References

- Spec: `docs/workflow_5_1_spec.md` (`af7b40d`)
- Engine: `~/.lux/workflows/nlm_feed_builder.py` v1.4
- URL classifier source: `~/.lux/workflows/extract_ai_links.py:21-46`
- Endpoints implementation: `~/.lux/workflows/alan_os_server.py` (`/ai_stack` block between `/competitors` and `/dashboard`)
- Storage: `~/.lux/Data/ai_stack_feed.json`
