# Loretta n8n Workflows — Status

Source: loretta-os repo — C:\Veritas\repos\loretta-os\
n8n endpoint: https://n8n.lorettasercy.com (VM, SecureAI-W11)

## Workflow Inventory

| Workflow | n8n ID | Status | Blocker |
|----------|--------|--------|---------|
| 2.1 Weekly Content Brief | `69lXVUnqWMr2yF1q` | ⏳ OAuth blocked | `gbwzaRu0ONWfhuUr` (Docs) + `sG8kOyb5bJb0hjgS` (Sheets reads unverified) |
| 2.2 YouTube Description Generator | `cLfHDVDl3tpZCaKQ` | ⏳ OAuth blocked | Same as 2.1 |
| 2.4 Video Repurposing | `tX09Uxf9LdjVLmvl` | ✅ Deployed, e2e blocked | 4 env vars + Loretta source video |
| 2.5 UTM Slug Generator | `jTY5fBQ0Nlb4GObd` | ⏳ OAuth blocked | `xkF1H9p5Q52UPPoi` trigger failing |
| 2.6 Content Intake Form | `kpkyWvM3OBLABOcl` | ⏳ OAuth blocked | Same as 2.5 |
| C — Telegram Topic Intake | `q0aogZju1nET96kP` | ✅ Active | Needs `setWebhook` curl call to wire Loretta's bot |

Also in repo (not Loretta-specific):
| 3.1 MMM Gmail Triage | `r1pkTZ94DuuWrTtA` | ✅ Active | — |
| 3.2 MMM Prospect Audit | `VvHYTjheeecJ441F` | ⚠️ Blocked | Sheets `__rl` node |
| AlanSercy MSN Flow | `7GEpqCGS2cP0J8wY` | Live | Likely email triage stack |

## OAuth Re-Auth Queue

Three Google credentials have revoked refresh tokens (since Apr 12–14 2026).
Re-auth must happen in n8n web UI: Credentials → click cred → Reconnect → complete Google consent.

| Cred ID | Name | Status | Blocks |
|---------|------|--------|--------|
| `sG8kOyb5bJb0hjgS` | Google Sheets account | Append works; reads/triggers unverified | 2.1, 2.2, 2.4, 2.5, 2.6, C |
| `xkF1H9p5Q52UPPoi` | Google Sheets Trigger account | Still failing | 2.5, 2.6 triggers |
| `gbwzaRu0ONWfhuUr` | Google Docs account | Unverified | 2.1, 2.2 |

**ngrok caveat:** ngrok free-tier URL rotates on every restart. When re-authing, the redirect URI
`https://unaltered-stiffly-renewably.ngrok-free.dev/rest/oauth2-credential/callback`
must be in Google Cloud Console → OAuth client → Authorized redirect URIs. Switch to paid ngrok
static subdomain or Cloudflare Tunnel to prevent recurring `redirect_uri_mismatch`.

## Workflow C — Telegram Intake Notes (Apr 26 debug)

**Live webhook URL:** `https://unaltered-stiffly-renewably.ngrok-free.dev/webhook/loretta-topic-intake`

**Trigger:** Regular `n8n-nodes-base.webhook` node (NOT telegramTrigger — that silently fails to register).
Loretta's bot needs manual setWebhook call:
```
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://unaltered-stiffly-renewably.ngrok-free.dev/webhook/loretta-topic-intake"
```

**Parse Topic:** Reads `$json.body.message` (webhook nests under `body`); fallback `$json.message` for telegramTrigger compatibility.

**Append schema:** Google Sheets append node requires `columns.schema` listing all 17 columns of Content Calendar. Schema copied from 2.2's `Write Description Doc Link` node.

**Verified end-to-end Apr 26:** Exec `13476` — webhook → Parse Topic → Skip Commands → Append succeeded (real row written to Content Calendar `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`). Reply:Added failed only because test used fake chat_id; bot token valid.

## Workflow 2.4 — Video Repurposing (deployed Apr 29)

**n8n ID:** `tX09Uxf9LdjVLmvl`
**Webhook:** `https://n8n.lorettasercy.com/webhook/video-repurpose` (POST)
**Source JSON:** `C:\Veritas\repos\alan-os\workflows\workflow_2_4_video_repurposing.json` (canonical)

**Blocked on (4 items before first run):**
1. `OPUS_CLIP_API_KEY` — set in n8n VM env (Settings → Environment). Source: opus.pro → Settings → API.
2. `BUFFER_ACCESS_TOKEN` — set in n8n VM env. Source: Buffer developer dashboard OAuth token.
3. `BUFFER_PROFILE_IDS` — set in n8n VM env. Comma-separated Buffer profile IDs.
4. Loretta source video — Loretta records and provides first MP4 URL.

**Also confirm before first run:**
- `Video Log` tab exists in Content Calendar `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`
  with columns: `Date | Video Title | Clips Generated | Platforms | Status | Buffer Response | Submitted At`

## Import / Deploy Reference

API keys are scrubbed to `{{ANTHROPIC_API_KEY}}` in repo. To re-import to n8n:
1. Replace `{{ANTHROPIC_API_KEY}}` with real key (or use n8n credential)
2. Import via n8n UI (Workflows → Import from File) or API:
```powershell
$body = Get-Content workflows/<id>.json -Raw
Invoke-RestMethod -Uri "https://n8n.lorettasercy.com/api/v1/workflows/<id>" `
  -Headers @{'X-N8N-API-KEY'=$env:N8N_API_KEY;'Content-Type'='application/json'} `
  -Method PUT -Body $body
```

n8n PUT accepts only: `name`, `nodes`, `connections`, `settings`.
Strip before PUT: `active`, `createdAt`, `updatedAt`, `versionId`, `tags`, `id`.
