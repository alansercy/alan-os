# Workflow 4.1 Spec — SalesOS Lead Enrichment (Hybrid C)

**Status:** SPEC — pending build
**Owner:** Alan Sercy / Veritas AI Partners
**Phase:** SalesOS Phase 1
**Last updated:** 2026-04-30

---

## Purpose

Take a `lead_id` referencing a row in the MMM Prospect Tracker Sheet, run web research via Claude, write enrichment back to the Sheet AND POST a normalized lead to the alan-os SalesOS API at `POST /leads`. This is the on-ramp into the SalesOS pipeline for MMM Trucking prospects — the Sheet stays the operational source of truth for Loretta/Nimrat, while `leads.json` carries the SalesOS-dashboard view.

This is the "hybrid C" design — Sheet-in / Sheet-out **and** SalesOS POST in the same flow. Both stores stay in sync at enrichment time.

## Trigger

Webhook only — `POST https://n8n.lorettasercy.com/webhook/salesos-enrich`.

Manual trigger node is wired in for ad-hoc testing in n8n UI; both paths converge on the normalized payload via Merge.

### Input contract

```json
{ "lead_id": "1" }
```

`lead_id` is the value in the `#` column (col B) of the `WA Prospect Tracker (n8n)` tab. Numeric or string. Required. No other fields accepted in V1.

## Sheet contract — MMM Prospect Tracker

**Spreadsheet:** `MMM_Trucking_Prospect_Tracker` · ID `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI`
**Tab (V1, only):** `WA Prospect Tracker (n8n)` — separate from the human `WA Prospect Tracker` tab so manual edits and machine writes don't collide.
**Header row:** row 3 (rows 1–2 are banner / context).
**Columns (A–S):** `Priority | # | Company | City / State | Address | Type | What They Ship | Known Ship-To (CA) | Est. Loads/Wk | Warm Intro? | Contact Name | Title / Role | Phone | Email | Outreach Status | Last Contact | Who Sent | Next Step | Notes`

Other tabs (`HP Hood Lane Tracker`, `Utah-Idaho Corridor`, `CA Receivers (Backhaul Intel)`, `Strategy & Key`) are out of scope for V1. Adding them = parameterize `sheetName` and add per-tab schema mapping.

## Steps

### Step 1 — Triggers + normalize

Nodes: **Webhook** + **Manual Trigger** → **Merge** → **Set: Normalize Input**.

Outputs single item:
```json
{ "lead_id": "<string>", "submitted_at": "<ISO timestamp>" }
```

If `lead_id` missing or empty: **IF: Validate Input** routes to a respond-400 path.

### Step 2 — Read row from Sheet

Node: **Google Sheets — Lookup row** (typeVersion 4.4 or higher)

- `documentId`: `__rl` wrapper, mode `id`, value `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI`
- `sheetName`: `__rl` wrapper, mode `name`, value `WA Prospect Tracker (n8n)`
- Operation: `lookup`
- Lookup column: `#`
- Lookup value: `={{ $json.lead_id }}`
- Header row: 3
- Data starts at row: 4
- Credential: existing `sG8kOyb5bJb0hjgS` ("Google Sheets account")

If no match: **IF: Row Found** routes to a respond-404 path with `{error: "lead_id not in tracker"}`.

### Step 3 — Build apiBody for Claude

Node: **Code — Build apiBody** (JavaScript)

```javascript
const row = $input.item.json;
const systemPrompt = `You are a B2B sales research assistant for MMM Trucking — a reefer-and-produce, asset-based, minority/women-owned carrier running NorCal → Washington → Utah/Idaho → SoCal/NorCal.

Given a Washington-state shipper prospect, return a JSON object with EXACTLY these fields and nothing else:
{
  "type": "<grower / packer / shipper / cold-storage / processor / etc.>",
  "what_they_ship": "<commodity description, year-round vs seasonal>",
  "known_ship_to": "<CA destinations / DCs / receivers if known>",
  "est_loads_per_week": "<range like 5-10 or 10-20, or '' if unknown>",
  "company_summary": "<2-3 sentence factual summary>",
  "fit_signal": "high" | "medium" | "low",
  "fit_rationale": "<1-2 sentence reason — lane fit, year-round volume, reefer needs, current carrier landscape>",
  "competitor_notes": "<who currently hauls for them if known, or '' >"
}
Output ONLY the JSON object, no preamble, no markdown fences.`;

const userPrompt = `Company: ${row['Company'] || ''}
City/State: ${row['City / State'] || ''}
Address: ${row['Address'] || ''}
Existing Type: ${row['Type'] || '(unknown)'}
Existing What They Ship: ${row['What They Ship'] || '(unknown)'}
Existing Known Ship-To (CA): ${row['Known Ship-To (CA)'] || '(unknown)'}
Existing Est. Loads/Wk: ${row['Est. Loads/Wk'] || '(unknown)'}
Existing Notes: ${row['Notes'] || '(none)'}

Research and return the JSON.`;

return [{
  json: {
    ...row,
    apiBody: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }]
    })
  }
}];
```

### Step 4 — HTTP Request to Anthropic

Node: **HTTP Request** (typeVersion 4.2)

Per CLAUDE.md §2 (non-negotiable):
- Method: POST
- URL: `https://api.anthropic.com/v1/messages`
- Headers:
  - `x-api-key`: `={{ $env.ANTHROPIC_API_KEY }}`
  - `anthropic-version`: `2023-06-01`
  - `content-type`: `application/json`
- `contentType`: `raw`
- Body: `={{ $json.apiBody }}`
- **Never** use the built-in Anthropic node. It does not work on this n8n install.

### Step 5 — Parse Claude response

Node: **Code — Parse Response** (JavaScript)

```javascript
const original = $('Step 2 — Lookup Row').item.json;
const apiResp  = $input.item.json;
const raw = apiResp.content?.[0]?.text || '{}';

let enriched = {};
try {
  enriched = JSON.parse(raw);
} catch (e) {
  const stripped = raw.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim();
  enriched = JSON.parse(stripped);
}

const today = new Date().toISOString().slice(0, 10);
const enrichedNoteBlock = [
  `[salesos-enrich ${today}]`,
  enriched.company_summary ? `Summary: ${enriched.company_summary}` : '',
  enriched.fit_signal ? `Fit: ${enriched.fit_signal} — ${enriched.fit_rationale || ''}` : '',
  enriched.competitor_notes ? `Competitors: ${enriched.competitor_notes}` : ''
].filter(Boolean).join('\n');

const existingNotes = original['Notes'] || '';
const mergedNotes = existingNotes
  ? `${existingNotes}\n\n${enrichedNoteBlock}`
  : enrichedNoteBlock;

const writeback = {
  '#': original['#'],
  Type:                 original['Type']                || enriched.type || '',
  'What They Ship':     original['What They Ship']      || enriched.what_they_ship || '',
  'Known Ship-To (CA)': original['Known Ship-To (CA)']  || enriched.known_ship_to || '',
  'Est. Loads/Wk':      original['Est. Loads/Wk']       || enriched.est_loads_per_week || '',
  Notes: mergedNotes
};

const salesosLead = {
  owner: 'alan',
  pipeline: 'mmm_trucking',
  source: 'mmm_prospect_tracker',
  company: original['Company'] || '',
  contact_name: original['Contact Name'] || '',
  contact_title: original['Title / Role'] || '',
  contact_email: (original['Email'] || '').includes('@') ? original['Email'] : '',
  contact_linkedin: '',
  stage: 'researched',
  last_contact: original['Last Contact'] || '',
  next_action: original['Next Step'] || '',
  next_action_date: '',
  notes: `[mmm:#=${original['#']}] ${mergedNotes}`
};

return [{
  json: {
    lead_id: original['#'],
    writeback,
    salesos_lead: salesosLead,
    enriched
  }
}];
```

### Step 6 — Update Sheet row (write-back)

Node: **Google Sheets — Update row** (same typeVersion as Step 2)

- `documentId` / `sheetName`: same `__rl` wrappers as Step 2
- Operation: `update`
- Match column: `#`
- Match value: `={{ $json.lead_id }}`
- Columns: define `Type`, `What They Ship`, `Known Ship-To (CA)`, `Est. Loads/Wk`, `Notes` from `$json.writeback.*`
- Header row: 3
- Credential: same `sG8kOyb5bJb0hjgS`

**Blank-only policy:** the four operational columns (Type / What They Ship / Known Ship-To / Est. Loads/Wk) are written only if the existing cell is blank — preserves Loretta's manual edits. The merge logic lives in the Step 5 Code node (`original['Type'] || enriched.type`).

**Notes always appends.** A re-run of the same `lead_id` will append a second `[salesos-enrich YYYY-MM-DD]` block to Notes.

### Step 7 — POST to alan-os /leads

Node: **HTTP Request** (typeVersion 4.2)

- Method: POST
- URL: `={{ $env.ALAN_OS_PUBLIC_URL }}/leads`
- Headers: `content-type: application/json`
- `contentType`: `raw`
- Body: `={{ JSON.stringify($json.salesos_lead) }}`
- Capture response `id` as `$json.salesos_lead_id` for the webhook response.

**`ALAN_OS_PUBLIC_URL`** is an env var on the n8n VM that points to the host's `localhost:8000` exposed via ngrok. Resolution decision (2026-04-30): ngrok over the other two options in the V0 spec (FastAPI `/admin/write-file`, move alan-os to VM). Alan sets the actual URL before first live run.

### Step 8 — Respond to webhook

Node: **Respond to Webhook**

Body:
```json
{
  "lead_id": "{{ $json.lead_id }}",
  "salesos_lead_id": "{{ $('Step 7 — POST /leads').item.json.id }}",
  "enriched": "{{ $json.enriched }}"
}
```

## Error handling

Every HTTP / Sheets node: `onError: continueErrorOutput`.

All error branches converge on a single **Gmail — Send Error** node:
- To: `alansercy@gmail.com`
- Subject: `[SalesOS 4.1] Error enriching lead_id={{ $json.lead_id }}`
- Body: failing node + error message + lead_id + timestamp.

Webhook still responds (500) with `{error: "<short tag>"}` so callers see the failure.

## Dedup

None in V1. Re-firing same `lead_id`:
- Sheet: appends a new `[salesos-enrich]` block to Notes; operational cols stay (blank-only policy).
- `/leads`: creates a duplicate record. The notes carry an `[mmm:#=N]` tag — Phase 2 `POST /leads` can dedup on that tag and skip the create.

## Credentials

| Credential | Status | Notes |
|---|---|---|
| Google Sheets — `sG8kOyb5bJb0hjgS` | Live | Read + update on `WA Prospect Tracker (n8n)` |
| `ANTHROPIC_API_KEY` (env) | Live | Already on VM |
| Gmail OAuth (Alan, alansercy@gmail.com) | Live | Used by 3.1 / 3.2 — error path only |
| `ALAN_OS_PUBLIC_URL` (env) | **To be set** | Alan sets ngrok URL before first live run |

## Validation

Run `mcp__n8n-mcp__validate_workflow` at profile `runtime` and resolve all errors before activation. `typeVersion` and `cachedResultName` warnings are non-blocking (per 2.4 deploy precedent).

## Mapping table — Sheet → SalesOS lead

| Sheet column | SalesOS field | Notes |
|---|---|---|
| (fixed) | `owner` | `"alan"` — this is Alan's SalesOS engine |
| (fixed) | `pipeline` | `"mmm_trucking"` |
| (fixed) | `source` | `"mmm_prospect_tracker"` |
| Company | `company` | |
| Contact Name | `contact_name` | |
| Title / Role | `contact_title` | |
| Email | `contact_email` | only if contains `@`; else blank |
| (none) | `contact_linkedin` | always blank in V1 |
| (fixed) | `stage` | `"researched"` |
| Last Contact | `last_contact` | |
| Next Step | `next_action` | |
| (none) | `next_action_date` | always blank in V1 |
| Notes + enrichment | `notes` | prefixed with `[mmm:#=N]` for Phase 2 dedup |

## Out of scope (Phase 2+)

- Dedup on `POST /leads` (`[mmm:#=N]` tag match)
- Adding new columns to `(n8n)` tab for `Company Summary` / `Fit Signal` / `Fit Rationale` / `Competitor Notes` (V1 compresses these inside Notes)
- Other tabs (HP Hood, Utah-Idaho, CA Receivers) — parameterize `sheetName` and per-tab schema
- Auto-trigger of an outbound sequencing agent when `fit_signal == high`
- Bulk webhook input (array of `lead_id`s)
- Competitor record creation from `competitor_notes` (would need `POST /competitors`, not yet built)

## Decisions locked (do not relitigate)

- Trigger: webhook only (`POST /salesos-enrich`); manual trigger for testing only
- Lead ID = `#` column (col B) on `(n8n)` tab
- Owner = `alan` (not Loretta — Loretta as sender stays in Sheet's `Who Sent` column as operational data)
- Blank-only write-back for the four operational columns; Notes always appends
- Compressed-in-Notes for V1 (no new Sheet columns until Phase 2)
- `(n8n)` tab only for V1
- VM→host resolution = ngrok via `ALAN_OS_PUBLIC_URL` env var
- Webhook response = `{lead_id, salesos_lead_id, enriched}` (small payload, not full row)
