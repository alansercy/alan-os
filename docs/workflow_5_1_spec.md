# Workflow 5.1 Spec — VIE Email Feed (Veritas Intelligence Engine V1)

**Status:** SPEC ONLY — not yet built
**Owner:** Alan Sercy / Veritas AI Partners
**Phase:** Veritas Intelligence Engine (VIE) — V1 (email-only)
**Architecture:** Python-first — extends `nlm_feed_builder.py` v1.4. **No new n8n workflow in V1.** n8n deferred to V2.
**Last updated:** 2026-04-29

---

## Purpose

Autonomous AI research radar. Walks MSN Outlook `Filing\` folders for new emails, extracts URLs, enriches each via Claude (summarize, score relevance, fit-tag against Veritas/AgentOS/PersonalOS pipelines), persists to `ai_stack_feed.json`, and surfaces a ranked dashboard panel. Replaces the manual "save link, read later, evaluate" loop with a continuously-running pipeline that pre-digests inputs before Alan ever sees them.

V1 ships email-only. V2 adds multi-source fan-in (GitHub trending, RSS, X/Twitter saves, Reddit) onto the same enrichment pipeline + storage + dashboard.

## Why Python-first (vs. an n8n workflow)

`C:\Users\aserc\.lux\workflows\nlm_feed_builder.py` v1.4 already implements ~80% of the V1 pipeline:
- Reads MSN > `Filing\{AI Research, Job Search, Veritas, Real Estate, MMM}` via Outlook COM
- Calls Claude Haiku per email with three folder-aware scoring prompts (`AI_STACK_PROMPT`, `VERITAS_PROMPT`, `JOB_STAGE1_PROMPT`)
- Has `unwrap_safelink()`, `extract_youtube_url()`, `extract_job_urls()` — Outlook Safe Links resolution included
- Persistent dedup at `.lux\Data\nlm_processed_ids.json`
- Pushes to 5 NotebookLM notebooks + appends to Veritas AI Research Feed Google Doc

The only gaps are (a) emitting per-URL enriched records to a JSON sink and (b) a dashboard surface. Building a parallel n8n flow that hits the same inbox would duplicate the Outlook reader, dedup registry, and Safelink unwrap logic for no functional gain. V2 is the right time to migrate to n8n once VIE earns multi-source inputs.

The legacy `ai_research_monitor.py` / `ai_research_backfill.py` pair (single-Doc target) is **not** the engine for V1 — `nlm_feed_builder.py` is the more comprehensive successor and is already scheduled per the v1.4 commentary. The legacy scripts stay in place for backfill/audit but VIE V1 does not augment them.

## Trigger

Same Task Scheduler entry that runs `nlm_feed_builder.py` (Sunday weekly per the v1.4 commentary). No new trigger required for V1.

For ad-hoc runs: `python C:\Users\aserc\.lux\workflows\nlm_feed_builder.py` from the host.

## Storage — `ai_stack_feed.json`

**Path:** `C:\Users\aserc\.lux\Data\ai_stack_feed.json` (capital D — matches `nlm_processed_ids.json` and `pending_jobs.json` casing in the same directory)

**Wrapped-object schema** (mirrors `leads.json` / `competitors.json` so `read_wrapped` / `write_wrapped` helpers in `alan_os_server.py:452-465` work unchanged):

```json
{
  "items": [
    {
      "id": "uuid4",
      "url": "https://example.com/article",
      "url_category": "YouTube|Anthropic|OpenAI|GitHub|n8n / Automation|AI Research|HBR / Strategy|Newsletter|LinkedIn|Real Estate|Other",
      "title": "Page title or email subject if not fetched",
      "summary": "Claude 1-3 sentence summary",
      "relevance_score": 0,
      "fit_pipeline": "ai_stack|veritas|agentos|personalos|loretta|mmm|none",
      "fit_rationale": "Why this scored where it did — one sentence",
      "tags": [],
      "status": "new",
      "source": {
        "type": "email",
        "email_hash": "md5 — same hash nlm_feed_builder uses for dedup",
        "folder": "ai_research|veritas|real_estate|mmm|job_search",
        "subject": "...",
        "sender": "...",
        "date": "YYYY-MM-DD"
      },
      "created_at": "ISO-8601",
      "updated_at": "ISO-8601"
    }
  ],
  "schema_version": "1.0",
  "last_updated": "ISO-8601"
}
```

**Schema choice — per-URL, not per-email:** the VIE charter ("ranked recommendations") wants the dashboard to rank links, not emails. One email with three URLs becomes three items, each with its own `relevance_score` and `fit_pipeline`. An email with zero URLs produces zero items (it's already captured by the existing nlm_feed_builder Doc + NotebookLM sinks).

**Field constraints:**
- `relevance_score`: integer 0–10 (10 = must-read for Alan now; 0 = noise)
- `fit_pipeline` enum: `ai_stack` | `veritas` | `agentos` | `personalos` | `loretta` | `mmm` | `none`
- `status` enum: `new` | `reviewed` | `saved` | `dismissed`
- `url_category` reuses the categorizer in `extract_ai_links.py:21-36`

## Steps

### Step 1 — Add a URL extractor to `nlm_feed_builder.py`

Add alongside the existing `extract_youtube_url()` / `extract_job_urls()`:

```python
AI_STACK_CATEGORIES = [
    ("YouTube",          r"youtube\.com|youtu\.be"),
    ("Anthropic",        r"anthropic\.com|claude\.ai"),
    ("OpenAI",           r"openai\.com|platform\.openai"),
    ("GitHub",           r"github\.com"),
    ("n8n / Automation", r"n8n\.io|zapier\.com|make\.com"),
    ("AI Research",      r"arxiv\.org|huggingface\.co|paperswithcode"),
    ("HBR / Strategy",   r"hbr\.org|sequoiacap\.com|a16z\.com"),
    ("Newsletter",       r"substack\.com|beehiiv\.com|therundown\.ai|lennysnewsletter"),
    ("LinkedIn",         r"linkedin\.com"),
    ("Real Estate",      r"nar\.realtor|inman\.com|tomferry|lofty\.com"),
    ("Other",            r".*"),
]

SKIP_URL_PATTERN = re.compile(
    r"(unsubscribe|tracking|pixel|click\.|redirect|utm_|mailchimp|"
    r"sendgrid|mandrillapp|postmark|cmail\.|r\.email|"
    r"images\.|\.(gif|png|jpg|jpeg|css|js|ico|woff)|"
    r"privacy|legal|terms|support\.google|accounts\.google|"
    r"mail\.google|calendar\.google)",
    re.IGNORECASE
)

def extract_ai_stack_urls(body: str) -> list[dict]:
    """Return [{url, category}] for each non-junk URL in body, Safelink-unwrapped."""
    out = []
    seen = set()
    for raw in re.findall(r'https?://[^\s<>"\']+', body):
        clean = raw.rstrip(".,;:!?)")
        resolved = unwrap_safelink(clean)
        if len(resolved) < 20 or SKIP_URL_PATTERN.search(resolved) or resolved in seen:
            continue
        seen.add(resolved)
        category = next((name for name, pat in AI_STACK_CATEGORIES
                         if re.search(pat, resolved, re.IGNORECASE)), "Other")
        out.append({"url": resolved, "category": category})
    return out
```

Logic ported from `extract_ai_links.py:21-46`; Safelink-unwrap is reused from `nlm_feed_builder.py:104-113`.

### Step 2 — Per-URL Claude enrichment

After an email passes the existing folder scoring (`score_email()`), call Claude once per extracted URL to produce the enriched record. Reuse the existing `CLAUDE_API_URL` / `CLAUDE_MODEL` / `httpx` plumbing.

**Prompt (constant `AI_STACK_URL_ENRICH_PROMPT`):**
```
You are enriching a URL for Alan Sercy's AI Stack research feed.

Alan runs:
- Veritas AI Partners (fractional CRO/BD for PE-backed AI companies)
- AgentOS (commercial AI OS for real estate agents)
- PersonalOS (personal AI operating system, Python + n8n)
- Loretta MoveWithClarity (real estate content brand)
- MMM Trucking (logistics SMB)

URL: {url}
URL category: {url_category}
Email subject: {subject}
Email sender: {sender}
Email body excerpt (first 800 chars): {body_excerpt}

Respond with JSON only, no preamble:
{
  "summary": "1-3 sentences on what this URL is and why it matters",
  "relevance_score": 0-10 integer,
  "fit_pipeline": "ai_stack|veritas|agentos|personalos|loretta|mmm|none",
  "fit_rationale": "one sentence on why this maps to that pipeline"
}
```

V1 does **not** fetch the URL — Claude works from email context alone. Page-fetch + content-extract per URL category lands in V2 once we know which categories repay the latency.

Parse with the same `try / strip-fences / retry` pattern used in `score_email()`.

### Step 3 — Append to `ai_stack_feed.json` via `POST /ai_stack`

Per enriched URL, POST to `http://localhost:8000/ai_stack` with the per-URL payload. The endpoint generates `id`, `created_at`, `updated_at`, defaults `status=new`, defaults `tags=[]`, and writes via `write_wrapped`.

`nlm_feed_builder.py` treats POST failures as non-fatal — the email's still in the existing `processed_ids` registry, so a retry won't re-enrich. Log a warning, continue to the next URL.

**Dedup at write time:** `POST /ai_stack` returns 200 with `{"dedup": true, "id": <existing_id>}` if an item with the same `url` already exists. This prevents duplicate records when the same URL appears across multiple emails (common with newsletter resends).

### Step 4 — `alan_os_server.py` endpoints

Add to the SalesOS section (mirror the `/leads` block at `alan_os_server.py:441-611`).

| Endpoint | Purpose |
|---|---|
| `GET /ai_stack` | List items. Query params: `status`, `fit_pipeline`, `min_score`, `category`, `limit` (default 100). Returns sorted by `relevance_score` desc, then `created_at` desc. |
| `POST /ai_stack` | Create item. Validates `fit_pipeline` ∈ enum, `status` ∈ enum, `relevance_score` 0–10. Generates `id` + timestamps. Dedups on `url`. |
| `PATCH /ai_stack/{id}` | Update `status` and/or `tags`. Bumps `updated_at`. Returns full updated item. |
| `GET /ai_stack/digest` | Top-N (default 10) `status=new` items by score for the dashboard panel. |

Pydantic models follow the `NewLead` / `LeadPatch` pattern. Enum constants (place near the existing `LEAD_*` constants):

```python
AI_STACK_PIPELINES = {"ai_stack", "veritas", "agentos", "personalos", "loretta", "mmm", "none"}
AI_STACK_STATUSES  = {"new", "reviewed", "saved", "dismissed"}
AI_STACK_CATEGORIES_ENUM = {"YouTube", "Anthropic", "OpenAI", "GitHub", "n8n / Automation",
                            "AI Research", "HBR / Strategy", "Newsletter", "LinkedIn",
                            "Real Estate", "Other"}
```

Register `GET /ai_stack/digest` BEFORE any `/ai_stack/{id}` route (same precedence rule the SalesOS `/leads/pipeline` route follows at `alan_os_server.py:498`).

### Step 5 — Dashboard panel

New tab in `C:\Users\aserc\.lux\dashboard\index.html` named **AI Stack**.

**Default view:** `GET /ai_stack/digest` — top 10 unread items by score.

**Full view:** `GET /ai_stack` — paginated table with filter chips for `fit_pipeline` + `status` + `category`.

**Per-row UI:**
- Title (links to URL, opens in new tab)
- Category badge | Pipeline badge | Score (color-coded: 0–3 grey, 4–6 yellow, 7–10 green)
- Summary (one line collapsed, full on hover/click)
- Source line: `[folder] sender · YYYY-MM-DD · email subject`
- Action buttons: **Save** (PATCH `status=saved`), **Dismiss** (PATCH `status=dismissed`), **Reviewed** (PATCH `status=reviewed`)
- Tag input (free-form, comma-separated, PATCH `tags`)

**Polling:** 60s while tab visible. Mirrors the existing `_n8n_cache` / SalesOS pattern.

## Error handling

- Claude enrichment failures (per URL): log a warning, skip that URL, continue. Email's still marked processed via the existing `nlm_processed_ids.json` registry.
- POST `/ai_stack` failures: log + skip. Same reasoning.
- Server is on `localhost` from the host's perspective — no VM↔host bridging issue. **This is the win vs. Workflow 4.1**, which still has open questions on the same hop.

## Credentials needed

| Credential | Status | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` (host env) | Live | Already loaded by `nlm_feed_builder.py` via `os.environ.get` |
| Outlook COM | Live | Already used by nlm_feed_builder |
| Google Docs service account | Already wired | Optional for V1 — keep the existing Veritas Feed Doc append running as a backup audit log |
| n8n API key / OAuth | **Not needed in V1** | Deferred to V2 |

## Validation / smoke test plan

1. Add `extract_ai_stack_urls()` + `AI_STACK_URL_ENRICH_PROMPT` + POST sink to `nlm_feed_builder.py`
2. Add `read_wrapped("ai_stack_feed.json", "items")` skeleton + 4 endpoints to `alan_os_server.py`; `curl -X POST http://localhost:8000/admin/restart`
3. Smoke test endpoints with a hand-crafted item before wiring nlm_feed_builder
4. Run `nlm_feed_builder.py` against a known AI-research email; confirm one item per URL appears in `ai_stack_feed.json` with all fields populated
5. Run twice; confirm dedup-on-url returns 200 with `dedup=true` and no duplicate row
6. Add dashboard tab; verify panel renders, score color thresholds correct, action buttons round-trip status

## Out of scope (V2+)

- **Multi-source fan-in** — GitHub trending, RSS feeds, X/Twitter saves, Reddit subscriptions. Same enrichment pipeline + storage + dashboard, new ingestors.
- **n8n migration** — once V2's multi-source fan-in lands, the orchestration is worth lifting into n8n with one workflow per source feeding a shared `POST /ai_stack` webhook.
- **URL fetch + content extract** — currently Claude scores from email context only. Fetch + Readability extract per URL category in V2.
- **Auto-promote `relevance_score >= 9` to a SalesOS lead** when `fit_pipeline ∈ {veritas, agentos}` — needs Phase 2 dedup logic on `/leads` first.
- **Telegram inline alert** for `score=10` items — would reuse the Daily Email Digest webhook pattern (`TOxyxAf39pjlRNfN`).
- **Per-pipeline NotebookLM mirror** — push enriched records into the existing 5 NotebookLM notebooks. nlm_feed_builder already has the auth + adapter; one-line wire later.

## Open questions (for V1 build session)

1. **Score calibration drift** — Claude `relevance_score` will drift across runs. V1 accepts the drift; V2 may need a known-good calibration batch.
2. **`extract_ai_links.py` retirement** — keep as parallel grep artifact, or retire once dashboard is live? Default: keep until dashboard lands.
3. **Backfill** — re-run nlm_feed_builder against existing 50–200 emails in MSN `Filing/AI Research`? Default: no backfill in V1; let the feed grow forward from first run.

## Build sequence

1. Add `/ai_stack` endpoints + `ai_stack_feed.json` skeleton to `alan_os_server.py` (mirror SalesOS Phase 1 pattern). Smoke-test with `curl`.
2. Augment `nlm_feed_builder.py`: add URL extractor, enrichment prompt + parser, POST sink.
3. End-to-end smoke test against a single AI-research email.
4. Build dashboard "AI Stack" tab.
5. Confirm scheduled run picks up the new sink without further changes.

## References

- Engine: `C:\Users\aserc\.lux\workflows\nlm_feed_builder.py` (v1.4, ~800 lines)
- URL category source: `C:\Users\aserc\.lux\workflows\extract_ai_links.py:21-46`
- Wrapped-object endpoint pattern: `C:\Users\aserc\.lux\workflows\alan_os_server.py:441-611` (`/leads`, `/competitors`)
- Sister spec: `docs/workflow_4_1_spec.md` (SalesOS lead enrichment — n8n-first, host-VM bridging concerns; VIE 5.1 sidesteps both by staying on the host)
- Project entry: `PROJECTS.md:610-636` (VIE roadmap)
