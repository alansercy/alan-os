# Workflow 4.1 Spec — SalesOS Lead Enrichment

**Status:** SPEC ONLY — not yet built
**Owner:** Alan Sercy / Veritas AI Partners
**Phase:** SalesOS Phase 1
**Last updated:** 2026-04-29

---

## Purpose

Take a target company / contact as input, run web research via Claude, extract a structured lead record, post it to the alan-os SalesOS API at `POST /leads`, and email a summary to Alan. This is the on-ramp into the SalesOS pipeline — every other stage assumes the lead already exists in `leads.json`.

## Trigger

Two trigger modes on the same workflow:

1. **Manual trigger** (n8n UI Execute Workflow) — for ad-hoc research on a single target. Input via "Edit Fields (Set)" node.
2. **Webhook trigger** — `POST https://n8n.lorettasercy.com/webhook/salesos-enrich` for programmatic input from the dashboard or a CSV-driven batch job later.

Both paths converge on a single normalized payload via a Merge node.

### Input contract

```json
{
  "company": "Acme Logistics",
  "contact_name": "Jane Doe",
  "contact_title": "VP of Operations",
  "contact_email": "",
  "contact_linkedin": "",
  "owner": "alan",
  "pipeline": "veritas_bd",
  "source": "research",
  "notes": ""
}
```

`owner` and `pipeline` are required; everything else is optional and will be enriched in Step 2.

## Steps

### Step 1 — Accept + normalize input

Node: **Edit Fields (Set)** + **Merge** (combine manual + webhook paths)
Output: single item with the normalized payload above. Validate required fields (`company`, `owner`, `pipeline`); fail-fast via IF node if missing.

### Step 2 — Web research via HTTP Request to Anthropic

Node: **HTTP Request** (typeVersion 4.2)

**Per CLAUDE.md Section 2 (non-negotiable):**
- Method: POST
- URL: `https://api.anthropic.com/v1/messages`
- Headers:
  - `x-api-key`: `={{ $env.ANTHROPIC_API_KEY }}`
  - `anthropic-version`: `2023-06-01`
  - `content-type`: `application/json`
- `contentType`: `raw`
- Body: `={{ $json.apiBody }}` (built in a preceding Code node — see below)
- **Never use the built-in Anthropic node.**

**Preceding Code node — build `apiBody`:**

```javascript
const input = $input.item.json;
const systemPrompt = `You are a B2B sales research assistant. Given a company name (and optionally a contact), return a JSON object with these fields and nothing else:
{
  "company": "...",
  "contact_name": "...",
  "contact_title": "...",
  "contact_email": "...",
  "contact_linkedin": "...",
  "competitor_notes": "...",
  "company_summary": "...",
  "fit_signal": "high|medium|low",
  "fit_rationale": "..."
}
Output ONLY the JSON object, no preamble, no markdown fences.`;

const userPrompt = `Pipeline: ${input.pipeline}
Owner: ${input.owner}
Company: ${input.company}
Known contact: ${input.contact_name || 'unknown'} (${input.contact_title || 'title unknown'})
Seed notes: ${input.notes || 'none'}

Research and return the JSON.`;

return [{
  json: {
    ...input,
    apiBody: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1024,
      system: systemPrompt,
      messages: [{ role: "user", content: userPrompt }]
    })
  }
}];
```

### Step 3 — Extract enriched fields

Node: **Code** (parse Claude response into a typed lead object)

```javascript
const original = $('Step 1 — Normalize').item.json;
const apiResp  = $input.item.json;

const raw = apiResp.content?.[0]?.text || '{}';
let enriched = {};
try {
  enriched = JSON.parse(raw);
} catch (e) {
  const stripped = raw.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim();
  enriched = JSON.parse(stripped);
}

const lead = {
  owner: original.owner,
  pipeline: original.pipeline,
  source: original.source || 'research',
  company: enriched.company || original.company,
  contact_name: enriched.contact_name || original.contact_name || '',
  contact_title: enriched.contact_title || original.contact_title || '',
  contact_email: enriched.contact_email || original.contact_email || '',
  contact_linkedin: enriched.contact_linkedin || original.contact_linkedin || '',
  stage: 'researched',
  competitor_notes: enriched.competitor_notes || '',
  notes: [
    original.notes,
    enriched.company_summary ? `Summary: ${enriched.company_summary}` : '',
    enriched.fit_signal ? `Fit: ${enriched.fit_signal} — ${enriched.fit_rationale || ''}` : ''
  ].filter(Boolean).join('\n\n')
};

return [{ json: { lead, fit_signal: enriched.fit_signal, fit_rationale: enriched.fit_rationale } }];
```

### Step 4 — POST to /leads endpoint

Node: **HTTP Request** (typeVersion 4.2)
- Method: POST
- URL: `http://host.docker.internal:8000/leads` — n8n runs on the VM; alan-os runs on the host. Reachable network path needs verification before first run; fallback options below.
- `contentType`: `raw`
- Body: `={{ JSON.stringify($json.lead) }}`
- Header: `content-type: application/json`
- Response: capture `id` from the JSON response — that is the SalesOS lead ID for the summary email.

**Open question (resolve before build):** does the n8n VM have a reachable path to `localhost:8000` on the host? If not, options are (a) expose alan-os via ngrok / Cloudflare Tunnel, (b) write directly to `leads.json` via the existing `/admin/write-file` endpoint, or (c) move alan-os onto the VM. Decide before first build.

### Step 5 — Summary email to Alan

Node: **Gmail — Send a message** (existing Gmail OAuth cred, alansercy@gmail.com)
- To: `alansercy@gmail.com`
- Subject: `[SalesOS] New lead: {{ $json.lead.company }} ({{ $json.lead.pipeline }})`
- Body:

```
SalesOS lead created.

Company:     {{ $json.lead.company }}
Pipeline:    {{ $json.lead.pipeline }}
Owner:       {{ $json.lead.owner }}
Contact:     {{ $json.lead.contact_name }} — {{ $json.lead.contact_title }}
Email:       {{ $json.lead.contact_email }}
LinkedIn:    {{ $json.lead.contact_linkedin }}
Stage:       researched
Fit:         {{ $json.fit_signal }} — {{ $json.fit_rationale }}

Competitor notes:
{{ $json.lead.competitor_notes }}

Notes:
{{ $json.lead.notes }}

Lead ID: {{ $('Step 4 — POST /leads').item.json.id }}
Dashboard: http://localhost:8000/dashboard#salesos
```

## Error handling

- Each HTTP node gets `onError: continueErrorOutput` so failures route to a single **Gmail — Send error email** node that emails Alan with the failing node name + error message + original input.
- The `/leads` POST is idempotent on the client side (no dedup yet — Phase 2 may add company-name dedup); a duplicate run will create two records. Alan reviews the summary email and can PATCH `stage=dead` on the dupe.

## Credentials needed

| Credential | Status | Notes |
|---|---|---|
| `ANTHROPIC_API_KEY` (env) | Live | Already on VM |
| Gmail OAuth (Alan) | Live | Same cred used by 3.1 / 3.2 |
| alan-os reachability from VM | Unverified | See Step 4 open question |

## Validation profile

When this is built, run `mcp__n8n-mcp__validate_workflow` at profile `runtime` and resolve all errors before activation. Warnings about `typeVersion` and `cachedResultName` are non-blocking per the 2.4 deploy precedent.

## Out of scope (Phase 2+)

- Dedup logic on `POST /leads` (company-name fuzzy match)
- Auto-trigger of an outbound sequencing agent when `fit_signal == high`
- Bulk CSV input via webhook batch
- Competitor record creation from `competitor_notes` (will need its own flow that POSTs to a future `POST /competitors`)
