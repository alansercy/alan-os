# VM — Infrastructure Reference (SecureAI-W11)

## Environment
- **Type:** Hyper-V VM on Host machine
- **Name:** SecureAI-W11
- **n8n endpoint:** https://n8n.lorettasercy.com
- **Local n8n (VM-internal):** localhost:5678 (not reachable from Host)

## Tunnel
- **ngrok** — free tier, URL rotates on every restart
- Current URL: `https://unaltered-stiffly-renewably.ngrok-free.dev`
- ⚠️ URL rotation causes OAuth `redirect_uri_mismatch` on re-auth — switch to paid static subdomain or Cloudflare Tunnel

## n8n
- **API key suffix:** J2g (same as Host .env N8N_API_KEY)
- **Workflow 4.1 ID:** `zl9peS1ZGNISLibZ`
- **Loretta Workflow C webhook:** `https://unaltered-stiffly-renewably.ngrok-free.dev/webhook/loretta-topic-intake`
- **Video Repurposing webhook:** `https://n8n.lorettasercy.com/webhook/video-repurpose`

## VM Repos
- `C:\Veritas\repos\` — mirrors Host repo structure
- Context always sourced from Host. VM executes only.

## VM Scripts (staged, not yet deployed)
Two PS1 scripts at `handoff/vm-scripts/` in alan-os repo:
- `01_register_n8n_autostart.ps1` — Task Scheduler entry for n8n auto-start
- `02_add_mmm_sheets_url.ps1` — writes corrected sheet ID to `.n8n\.env`

Deployment is manual paste — n8n filesystem writes are blocked everywhere on VM.
Paste into elevated PowerShell on VM to deploy.

## n8n Technical Rules (non-negotiable)

- **HTTP Request to Anthropic:** typeVersion 4.2, `x-api-key`, `anthropic-version: 2023-06-01`, contentType raw, body via `={{ $json.apiBody }}`. Never the built-in Anthropic node.
- **Google Sheets nodes:** `documentId` and `sheetName` always via `__rl` resource locator wrapper. No raw IDs.
- **n8n API PUT:** strip `active`, `createdAt`, `updatedAt`, `versionId`, `tags`, `id` before sending.
- **Email sanitization:** strip `/[\x00-\x1F\x7F-\xFF<>"\\]/g`, join with `||` not `\n`.
- **Gmail field names:** capitalized — `From`, `Subject`.
- **Deploy fallback:** n8n UI browser console (Ctrl+Shift+J, allow pasting).
- **Never deploy a workflow change without testing in n8n UI first.**
- **Ask before any action that touches credentials.**

## HTML Prototype Path (VM-resident)
`C:\Users\SecureAI-W11\Projects\loretta-site\` — exists on VM, not accessible from Host.
