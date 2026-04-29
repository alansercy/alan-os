# SalesOS Dashboard Tab Spec

**Status:** SPEC ONLY — not yet built
**Target file:** `C:\Users\aserc\.lux\dashboard\index.html` (or `claude_usage_dashboard.html` if that path is canonical — verify before build)
**Phase:** SalesOS Phase 1
**Last updated:** 2026-04-29

---

## Purpose

A new **SalesOS** tab in the Alan OS dashboard that shows the live pipeline as a kanban board, scoped per pipeline (Veritas BD / Loretta RE / MMM Trucking), with a collapsible competitor intel panel underneath. Read-only first pass except stage transitions and quick-edits to `next_action`. Backed entirely by the new `/leads`, `/leads/pipeline`, and `/competitors` endpoints added in Phase 1.

## Tab placement

New top-level tab labeled **SalesOS** in the existing dashboard nav, sitting alongside the current panels (Projects, Tasks, n8n, Knowledge, etc.). Default landing state: pipeline filter = `veritas_bd`, owner filter = "all".

## Layout

```
+--------------------------------------------------------------------------+
| SalesOS                                          [+ New Lead]  [Refresh] |
+--------------------------------------------------------------------------+
| Pipeline: [veritas_bd v]    Owner: [all v]    Stage filter: [all v]      |
+--------------------------------------------------------------------------+
|                          KANBAN BOARD (7 columns)                        |
|  +----------+----------+----------+----------+----------+----------+--+  |
|  | prospect |researched|contacted |responded |qualified | closed   |..|  |
|  |   (3)    |   (2)    |   (1)    |   (0)    |   (1)    |   (0)    |..|  |
|  +----------+----------+----------+----------+----------+----------+--+  |
|  | [Card]   | [Card]   | [Card]   |          | [Card]   |          |..|  |
|  | [Card]   | [Card]   |          |          |          |          |..|  |
|  | [Card]   |          |          |          |          |          |..|  |
|  +----------+----------+----------+----------+----------+----------+--+  |
+--------------------------------------------------------------------------+
| > Competitor Intel (collapsed)                                           |
+--------------------------------------------------------------------------+
```

## Filters (top bar)

| Filter | Values | Notes |
|---|---|---|
| Pipeline | `veritas_bd`, `loretta_re`, `mmm_trucking` | Single-select dropdown. No "all" — pipeline drives competitor panel scoping. Default: `veritas_bd`. |
| Owner | `all`, `alan`, `loretta`, `mmm` | Single-select. |
| Stage | `all` + each of the 7 stages | Hides columns when filtering to one stage; useful for export views later. |

State of all three filters held in component state and synced to URL query params (`?pipeline=...&owner=...`) so a refresh keeps context.

## Kanban columns

Seven columns, one per stage value, in the order from the data schema:

`prospect -> researched -> contacted -> responded -> qualified -> closed -> dead`

Column header: stage name + count badge. The 7th column (`dead`) is collapsed by default behind a "Show dead (N)" toggle to keep the active pipeline visually clean.

**Data source:** `GET /leads/pipeline?pipeline={pipeline}&owner={owner}` — already returns leads grouped by stage with counts. One request per render; no client-side grouping needed.

## Lead cards

Each card shows:

- **Company** (bold, top line)
- **Contact name** + title (one line, secondary color)
- **Last contact** (relative date — "3d ago", "2w ago"; falls back to absolute YYYY-MM-DD if blank)
- **Next action** (if set, in accent color) + **next_action_date** as small chip
- Owner pill in the corner (`alan` / `loretta` / `mmm` colored differently)
- **Source icon** (linkedin / referral / inbound / research)

Click a card -> opens a side-drawer with the full lead record, all fields editable, scrollable notes pane, Save button hits `PATCH /leads/{id}`.

**Stage transitions:** drag-and-drop between columns is Phase 2. For Phase 1, stage changes via the side-drawer's stage dropdown (PATCH on save). Cheap to ship.

## "New Lead" button

Top-right button -> modal with the `POST /leads` form. Required fields highlighted: `owner`, `pipeline`, `company`. Optional fields collapsed under a "More fields" expander to keep the modal small. Submit -> POST -> on success, refresh kanban + close modal + flash a "Lead created" toast with the new ID.

## Competitor Intel panel

Collapsible (collapsed by default), placed below the kanban. When expanded:

- Header: "Competitor intel for {pipeline}" (scoped by the top-bar pipeline filter)
- Grid of competitor cards:
  - **Name** + website link
  - **Strengths** (chip list, green)
  - **Weaknesses** (chip list, red)
  - **Positioning** (1-2 lines)
  - **Last researched** (date, with "stale" badge if > 90 days)
- Click a card -> side-drawer with full record + notes (read-only Phase 1; edits Phase 2)

**Data source:** `GET /competitors?pipeline={pipeline}` — already implemented. Empty state: "No competitor records yet for {pipeline}. Add via `POST /competitors` (not yet wired in UI)."

## States to handle

- **Empty state per column:** subtle "No leads in this stage" placeholder
- **Empty pipeline:** big empty state in the board area: "No leads yet for {pipeline}. Run Workflow 4.1 to enrich the first one."
- **Loading:** skeleton cards (3 per column) while `/leads/pipeline` is in flight
- **API error:** banner at top "Failed to load leads — check that alan_os_server is running" + Retry button
- **Filter combination yielding zero:** "No leads match owner={owner} in pipeline={pipeline}." with a Clear filters link

## Color tokens (reuse existing dashboard palette)

| Element | Token |
|---|---|
| Pipeline accent — `veritas_bd` | Navy `#0B1E3D` |
| Pipeline accent — `loretta_re` | Sage `#7A9E7E` |
| Pipeline accent — `mmm_trucking` | Steel `#4A5568` |
| Stage column header bg | dashboard's existing `--panel-bg` |
| Card bg | `--card-bg` (existing) |
| `next_action` chip | accent gold `#C6A96A` |
| Owner pill — alan | navy text on light grey |
| Owner pill — loretta | sage text on light grey |
| Owner pill — mmm | steel text on light grey |

If the dashboard doesn't yet have these tokens centralized, the SalesOS build session is the right time to extract them into a `:root` block.

## API contract reference (already shipped, Phase 1)

| Method | Path | Purpose |
|---|---|---|
| GET | `/leads` | List with optional `owner` / `pipeline` / `stage` filters |
| GET | `/leads/pipeline` | Grouped by stage — primary kanban data source |
| POST | `/leads` | Create from "New Lead" modal |
| PATCH | `/leads/{id}` | Side-drawer save |
| GET | `/competitors` | Competitor panel — optional `pipeline` filter |

## Out of scope (Phase 2+)

- Drag-and-drop stage changes
- Inline card edits without opening the drawer
- Competitor record create/edit UI (`POST /competitors`, `PATCH /competitors/{id}`)
- Lead -> competitor linking (which competitors are mentioned in which leads)
- Activity timeline per lead (calls, emails, notes with timestamps)
- CSV export per filter view
- Bulk stage transition (multi-select)
- Search across lead notes / competitor positioning text

## Build estimate

One Claude Code session, ~60-90 min:
1. Add the SalesOS tab + nav entry (10 min)
2. Filters + kanban grid + cards (30 min)
3. Side-drawer with PATCH (15 min)
4. New Lead modal with POST (15 min)
5. Competitor panel — read-only grid (10 min)
6. Empty / loading / error states (10 min)

Test plan: create 2-3 leads via curl, verify they appear correctly, drag through stages via the side-drawer, open competitor panel, refresh and verify URL state is preserved.
