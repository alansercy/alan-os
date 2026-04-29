# SalesOS Dashboard Tab Spec

**Status:** V1 SHIPPED 2026-04-29 (table view) — kanban deferred to V2
**Target file:** `C:\Users\aserc\.lux\claude_usage_dashboard.html` (Lux Command Center on `localhost:8081`)
**Phase:** SalesOS Phase 1
**Last updated:** 2026-04-29

---

## Purpose

A new **SalesOS** tab in the Lux Command Center showing leads as a sortable table with stage / pipeline / owner filters, plus a competitor intel grid filtered by the same pipeline. Read-only V1. No backend changes — everything reads from the existing `/leads` and `/competitors` endpoints in `alan_os_server.py` (port 8000) via the already-open CORS allow-list.

## Why a table, not a kanban

The original spec called for a 7-column kanban with side-drawer stage transitions. V1 ships a simpler **sortable table** instead because:

- Faster to ship (one panel, one fetch, no drag/drop scaffolding)
- Easier to scan when the pipeline is empty or sparse — kanban columns of 0 leads are visual noise
- Stage transitions are deferred to V2 anyway in the original spec (drag/drop was Phase 2, side-drawer was Phase 1) — table + filter is functionally equivalent for browsing
- Stage values still appear as colored badges, so the visual semantics carry over

The kanban remains a valid V2 — the same endpoints support both.

## Live state confirmed before build

- Lux Command Center is `~/.lux/claude_usage_dashboard.html` served on **port 8081** by `~/.lux/claude_usage_dashboard.py`
- Alan OS server (`alan_os_server.py`) on **port 8000** ships CORS `allow_origins=["*"]` so 8081 → 8000 fetches work directly
- Existing tabs: automation, projects, tasks, n8n, digest, vault — SalesOS slots after vault
- Brand kit already centralized: `--navy #0B1E3D`, `--navy-deep #061328`, `--gold #C6A96A`, `--surface #0F2548`, plus `--green/amber/red/idle` for status colors

## Tab placement

New nav button labeled **SalesOS** after `vault`. Sets `data-tab="salesos"`, content section `id="tab-salesos"`.

## Layout

```
+------------------------------------------------------------+
| Filters bar                                                |
|  Pipeline [all ▾]  Owner [all ▾]  Stage [all ▾]   [Refresh]|
+------------------------------------------------------------+
| Leads · N total · M after filter                           |
|  +------------------------------------------------------+  |
|  | Company | Contact | Stage | Last contact | Next acti |  |
|  |  ...    |   ...   |  ...  |    ...       |    ...    |  |
|  +------------------------------------------------------+  |
+------------------------------------------------------------+
| Competitor intel · scoped to {pipeline}                    |
|   [card] [card] [card] ...                                 |
+------------------------------------------------------------+
```

## Filters

| Filter | Values | Sent to endpoint |
|---|---|---|
| Pipeline | `all`, `veritas_bd`, `loretta_re`, `mmm_trucking` | `?pipeline=` (omitted if `all`) |
| Owner | `all`, `alan`, `loretta`, `mmm` | `?owner=` (omitted if `all`) |
| Stage | `all`, `prospect`, `researched`, `contacted`, `responded`, `qualified`, `closed`, `dead` | `?stage=` (omitted if `all`) |

Filters held in module-local state. Selection triggers an immediate refetch + re-render. No URL sync in V1 (YAGNI; can add later if Alan wants share-links).

## Mapping note (versus original ask)

The user request named `status (new/contacted/qualified/closed)`, `last_activity`, and `score`. Mapped to the actual schema:

| Asked | Built | Reason |
|---|---|---|
| Status filter (4 values) | Stage filter (7 values) | Schema field is `stage`. Collapsing 7 → 4 would silently hide leads in `prospect`/`researched`/`responded`/`dead`. |
| `last_activity` | `last_contact` | Same intent, schema's name. |
| `score` column | Omitted V1 | No score field exists on leads. Workflow 4.1 (deferred) is what would add `relevance_score`. Re-add the column when 4.1 lands. |

## Lead table

Columns:

| Column | Source | Render |
|---|---|---|
| Company | `company` | bold |
| Contact | `contact_name` + `contact_title` | name (top), title (muted, smaller) |
| Stage | `stage` | colored `.badge` (see palette below) |
| Last contact | `last_contact` | relative ("3d ago") with absolute as tooltip; "—" if blank |
| Next action | `next_action` + `next_action_date` | text + small date chip; "—" if blank |
| Owner | `owner` | small `.badge.gold` pill |
| Pipeline | `pipeline` | small muted text |

Sortable by clicking any column header (client-side; toggle asc/desc). Default sort: `last_contact desc` (most recent activity first), then `created_at desc` as tiebreak.

### Stage badge palette

| Stage | Badge class |
|---|---|
| `prospect` | `.badge.idle` |
| `researched` | `.badge.idle` |
| `contacted` | `.badge.amber` |
| `responded` | `.badge.amber` |
| `qualified` | `.badge.gold` |
| `closed` | `.badge.green` |
| `dead` | `.badge.red` |

## Competitor intel grid

Below the lead table, in its own `.panel`:

- Header: `Competitor intel · {pipeline}` (or `· all pipelines` when filter is `all`)
- Card grid (reuses `.vault-grid` class for consistency):
  - **Name** + website link (if present)
  - **Strengths** as `.badge.green` chips
  - **Weaknesses** as `.badge.red` chips
  - **Positioning** (1-2 lines)
  - **Last researched** (date, with "stale" amber pill if > 90 days)
- Empty state: `No competitor records yet.` (V1 has no UI to add — `POST /competitors` deferred to V2)

## States

| State | Treatment |
|---|---|
| Loading | `<div class="empty">Loading leads…</div>` (matches existing tab pattern) |
| API error | `.error-box` banner with the error message |
| Empty after filter | `No leads match these filters.` with Clear filters button |
| Empty pipeline globally | `No leads yet. Create one via POST /leads or run Workflow 4.1 once it ships.` |

## Refresh + counts

- `loadSalesOS()` joins `Promise.allSettled` in `refreshAll()` (60s interval already in place)
- Nav badge `count-salesos` shows total active leads (everything except `closed` and `dead`)
- Manual refresh = the existing top-right `↻` button

## API contract reference

| Method | Path | Purpose |
|---|---|---|
| GET | `/leads?owner=&pipeline=&stage=` | Table data |
| GET | `/competitors?pipeline=` | Competitor grid |

## Out of scope (V2+)

- Kanban view + drag-and-drop stage transitions
- Side-drawer with full lead edit + `PATCH /leads/{id}`
- New Lead modal (`POST /leads`)
- Competitor record create/edit (`POST /competitors`, `PATCH /competitors/{id}`)
- Score column (blocked on Workflow 4.1)
- URL state sync for filters
- CSV export
- Search across notes
- Activity timeline per lead

## V1 build estimate

~30-45 min in one Claude Code session. Single file edit (`claude_usage_dashboard.html`), no server changes.

## V1 test plan

1. POST a couple of test leads via curl across pipelines/owners
2. Open `localhost:8081`, click SalesOS tab → table renders, badge counts correct
3. Filter by pipeline → competitor section relabels + filters
4. Filter by stage → table filters
5. Sort by clicking column headers
6. Refresh button reloads
7. DELETE the test leads (or leave 1-2 as fixtures)
