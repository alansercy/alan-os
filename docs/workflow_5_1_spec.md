# Workflow 5.1 Spec — VIE V1 (Email → AI Stack Feed)

**Status:** SPEC ONLY — not yet built (substantial Python prior art exists, see "Existing assets")
**Owner:** Alan Sercy / Veritas AI Partners
**Phase:** Veritas Intelligence Engine (VIE) — V1
**Last updated:** 2026-04-29

---

## Purpose

Replace the manual "save link, read later, evaluate" loop with a continuously-running pipeline that scans Outlook inboxes for AI-related research, enriches each item via Claude (summarize, categorize, score relevance against Veritas / AgentOS / PersonalOS pipelines), and surfaces ranked recommendations on the alan-os dashboard.

**V1 scope:** email-only input. Proves the enrichment + ranking + surface loop end-to-end.
**V2 scope (out of scope here):** multi-source fan-in — GitHub trending, RSS, X/Twitter saves, Reddit. Same enrichment pipeline, additional collectors.

## Versioning + transport decision

| Version | Transport | Trigger | Sink | Status |
|---|---|---|---|---|
| **V1** | **Python** (Outlook COM + `anthropic` SDK + Google Docs API) | Task Scheduler — daily 7am | `ai_stack_feed.json` (NEW) **AND** Veritas AI Research Feed Doc (existing) | THIS SPEC |
| V2 | n8n HTTP Request to Anthropic per CLAUDE.md §2 (typeVersion 4.2, `x-api-key`, raw body) | n8n Schedule Trigger | Same `ai_stack_feed.json` via `POST http://host:8000/ai_stack` | Future — after VM↔host reachability resolved (same blocker as Workflow 4.1 Step 4) |

**Why Python first:** ~70% of V1 already exists in `~/.lux/workflows/ai_research_monitor.py` and `extract_ai_links.py`. The net-new piece is JSON emission and the dashboard panel. Building V1 in Python ships the loop in hours; rebuilding in n8n now would discard working code and hit the host-reachability blocker that's also gating Workflow 4.1.

## Existing assets (do not rebuild)

| File | Role in V1 |
|---|---|
| `~/.lux/workflows/ai_research_monitor.py` | **Augment** — already does daily Outlook scan + Claude Haiku summary + Google Doc append. Add a second sink: build a structured record per email and append to `ai_stack_feed.json`. |
| `~/.lux/workflows/ai_research_backfill.py` | Twin of monitor; same augmentation applies if backfill is re-run. |
| `~/.lux/workflows/extract_ai_links.py` | URL extraction reference — its categorization regex (14 categories, skip-pattern for trackers) becomes the URL-extraction step in the augmented monitor. |
| `~/.lux/workflows/nlm_feed_builder*.py` | Adjacent; pushes to NotebookLM. Out of scope for VIE V1 — leave running. |

## Canonical Google Doc

**Decision:** the only canonical AI research feed doc is `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M` ("Veritas AI Research Feed", owned by alansercy@gmail.com, registered in `drive_registry` and `ASSET_URLS` in `alan_os_server.py`).

The legacy doc `1f3RGBRlmFr7b4Mb-94RoAydAn3ClnmjFN2eO7VLeVyg` previously written to by `ai_research_monitor.py` and `ai_research_backfill.py` is **abandoned**. Historical summaries written there are not migrated. Going forward, both scripts write to `1WD2Sr2H...`. (See "Cutover notes" below.)

## Watched email sources

Keep the existing source list:
- `asercy@msn.com` — `Inbox`, `Inbox/Filing/AI Research`, `Inbox/Job Search`
- `alansercy@gmail.com` — `Inbox`, `Inbox/JobSearch`, `Inbox/AI Stack`
- `asercy@icloud.com` — when present in Outlook profile

Pre-filter: `RESEARCH_KEYWORDS` whitelist (already defined in `ai_research_monitor.py`) to keep Claude calls cheap. Skip-pattern for tracking pixels / unsubscribe links from `extract_ai_links.py`.

## Steps

### Step 1 — Scan inbox (existing)

`ai_research_monitor.py:get_inbox()` already does this. No change.

### Step 2 — Extract URLs from each candidate email (NEW — port from `extract_ai_links.py`)

For every candidate email after pre-filter, run the URL pattern (`https?://[^\s<>"'\)\]]+`) over `Body + HTMLBody`, apply `SKIP_PATTERN` to drop tracker / unsubscribe / image links, dedup against `~/.lux/ai_links_seen.txt` (existing registry).

Each remaining URL becomes a `links[]` entry on the ai_stack record. An email with zero URLs still produces a record (tagged `kind: "insight"` instead of `kind: "link"`).

### Step 3 — Enrich via Claude (existing, structured output expanded)

Use the existing `summarize_email()` Claude Haiku call. **Expand the prompt** to also return:
- `relevance_score` — integer 0–100
- `fit_tags` — array, subset of: `veritas_bd`, `agentos`, `personalos`, `tradeos`, `mmm_trucking`, `loretta_re`, `job_search`, `general_ai`
- existing fields: `category`, `key_points`, `action`

Enforce structured-JSON output (no prose). Parse with the same `try / strip-fences / retry` pattern used in Workflow 4.1 Step 3.

### Step 4 — Append to canonical Google Doc (existing, fix doc ID)

`append_to_doc(GOOGLE_DOC_ID, ...)` already runs. **Change** `GOOGLE_DOC_ID` constant in both `ai_research_monitor.py` and `ai_research_backfill.py` from `1f3RGBRl...` to `1WD2Sr2H...`. Format unchanged.

### Step 5 — Append to `ai_stack_feed.json` (NEW)

After successful Doc append, build the structured record (schema below) and append to `~/.lux/data/ai_stack_feed.json` via the new `POST /ai_stack` endpoint on `alan_os_server.py`. Failures here MUST NOT block Doc appends — the JSON sink is best-effort, the Doc is the durable record.

### Step 6 — Surface on dashboard (NEW — separate ticket)

New "AI Stack" panel on the dashboard. Lists last 50 items, sortable by `relevance_score`, filterable by `fit_tags` and `category`. Click-through opens the URL or a drawer with the full summary. Mark reviewed / promote to a SalesOS lead / dismiss.

This step is a separate dashboard work item, sized after V1 backend is live.

## `ai_stack_feed.json` schema

Wrapped-object format (mirrors `leads.json` / `competitors.json`):

```json
{
  "items": [
    {
      "id": "uuid-v4",
      "kind": "link" | "insight",
      "email_id": "Outlook EntryID — for dedup against backfill_tracker",
      "subject": "...",
      "sender_name": "...",
      "sender_email": "...",
      "received_at": "ISO-8601",
      "source_folder": "msn>Inbox>Filing>AI Research",
      "links": [
        { "url": "...", "category": "Anthropic" }
      ],
      "category": "AI Research" | "Job Opportunity" | "Industry Intel" | "Veritas Business" | "Real Estate" | "Newsletter" | "Other",
      "relevance_score": 0,
      "fit_tags": ["veritas_bd", "agentos"],
      "summary": "...",
      "key_points": ["...", "..."],
      "action": "None",
      "status": "new" | "reviewed" | "promoted" | "dismissed",
      "promoted_lead_id": null,
      "created_at": "ISO-8601",
      "updated_at": "ISO-8601"
    }
  ],
  "schema_version": "1.0",
  "last_updated": "ISO-8601"
}
```

## API endpoints (add to `alan_os_server.py`)

Mirror the SalesOS `/leads` pattern exactly. Use the existing `read_wrapped` / `write_wrapped` helpers — the wrapped-object schema fits.

| Method + Path | Purpose |
|---|---|
| `GET /ai_stack` | List items, optional filters: `?status=new`, `?category=X`, `?fit_tag=veritas_bd`, `?min_score=70`. Default returns last 50 sorted by `received_at` desc. |
| `POST /ai_stack` | Create item. Payload matches schema above minus `id` / `created_at` / `updated_at` / `status` (defaults to `new`). Validates `kind` and `category` against enums. |
| `PATCH /ai_stack/{id}` | Patch `status`, `fit_tags`, `relevance_score`, `promoted_lead_id`. Bumps `updated_at`. |
| `GET /ai_stack/by_score` | Returns top N items by `relevance_score` for "ranked recommendations" dashboard tile. |

Validation enums:
- `STACK_KINDS = {"link", "insight"}`
- `STACK_CATEGORIES = {"AI Research", "Job Opportunity", "Industry Intel", "Veritas Business", "Real Estate", "Newsletter", "Other"}`
- `STACK_STATUSES = ["new", "reviewed", "promoted", "dismissed"]`
- `STACK_FIT_TAGS = {"veritas_bd", "agentos", "personalos", "tradeos", "mmm_trucking", "loretta_re", "job_search", "general_ai"}`

## Cutover notes (Doc ID fix)

When the Doc ID flips from `1f3RGBRl...` to `1WD2Sr2H...`:
- The `backfill_tracker.json` `processed_ids` list still works as dedup — those Outlook EntryIDs are not in either doc, but the tracker prevents re-processing regardless of which doc is downstream
- Historical summaries previously written to `1f3RGBRl...` are NOT migrated; they remain in that doc as a frozen archive
- If a complete history is wanted in `1WD2Sr2H...`, run `ai_research_backfill.py` after deleting the relevant entries from `processed_ids` (or run with a `--force` flag — TODO if needed)
- Confirm canonical doc has the service account `lux-automation@lux-host-493415.iam.gserviceaccount.com` shared with edit access (already true — `nlm_feed_builder.py` writes there today)

## Error handling

Per-step error policy:
- Outlook COM error → log, abort run, no partial writes
- Claude API error on a single email → log, skip email, continue with next
- Google Doc append error → log, skip JSON write for that email, continue (Doc is the durable record — if it failed, do not record a "shipped" state in JSON)
- JSON write error → log, do NOT roll back Doc write (Doc append is idempotent enough; user can resync from Doc later)

## Credentials needed

| Credential | Status | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` | Live | Workspace key in `~/.lux/.env` |
| Google Docs OAuth (alansercy) | Live | `~/.lux/data/google_credentials.json` + `google_token.json` |
| Service account (alt path) | Live | `~/.lux/credentials/service_account.json` already used by `nlm_feed_builder.py`. V1 uses OAuth — service account is the n8n V2 path |
| Outlook COM access | Live | Outlook must be running for `win32com` |

## Schedule

Task Scheduler entry (mirror `Norman Inbox Guard`):
- **Trigger:** daily 7:00 AM (after Norman Guard 6:00 AM)
- **Action:** PowerShell → `python C:\Users\aserc\.lux\workflows\ai_research_monitor.py`
- **Working dir:** `C:\Users\aserc\.lux\workflows`
- **Run whether logged on or not:** No (needs Outlook session)
- **Idempotent:** yes — `processed_ids` tracker dedups, JSON writes are appends keyed by `email_id`

## Out of scope for V1 (V2+)

- Multi-source collectors (GitHub trending, RSS, X saves, Reddit) — V2 fan-in
- n8n transport — V2 upgrade once VM↔host reachability resolved (shared blocker with Workflow 4.1 Step 4)
- Auto-promote `relevance_score >= 90` items to SalesOS leads — Phase 3
- Per-`fit_tag` digest emails — Phase 3
- Vector search over the JSON corpus — Phase 4

## Open questions

1. Does `relevance_score` need calibration? V1 Claude scores will drift across runs; consider posting calibration prompts (a known-good item batch) and normalizing.
2. Should `extract_ai_links.py` legacy text-output be retired, or kept as a parallel artifact for grep-friendly review? Default: keep until dashboard panel is live.
3. Backfill strategy for existing 50-200 emails in MSN `Filing/AI Research` against `ai_stack_feed.json` — re-run `ai_research_backfill.py` once it's augmented, or one-shot import script? Default: re-run backfill, accept duplicate Doc entries (cosmetic).

## Build sequence

1. **THIS COMMIT** — Doc ID fix in `ai_research_monitor.py` + `ai_research_backfill.py` (no schema change, no new deps)
2. Add `/ai_stack` endpoints to `alan_os_server.py` + create `ai_stack_feed.json` skeleton (mirror SalesOS Phase 1 pattern)
3. Augment `ai_research_monitor.py`: expand Claude prompt for `relevance_score` + `fit_tags`, build structured record, POST to `/ai_stack`
4. Smoke test against current MSN inbox (single email round-trip)
5. Re-run `ai_research_backfill.py` against canonical doc (optional — see Open Question 3)
6. Build dashboard "AI Stack" panel (separate ticket)
7. Schedule Task Scheduler entry
