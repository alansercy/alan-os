# Memory Bank — Session Log

## 2026-04-28 Setup Session
- Installed n8n-mcp MCP server pointed at n8n.lorettasercy.com
- Installed n8n-skills into ~/.claude/skills/
- Initialized memory-bank protocol in CLAUDE.md
- Workflow 3.2 passed live run this session (Google Sheets cred reconnected as loretta.keysandcommunity@gmail.com)
- Next: Verify 3.1 active, deploy 2.4

## 2026-04-28 n8n MCP Smoke + 2.4 Deploy Attempt
- What was done
  - Confirmed n8n-mcp connected via mcp__n8n-mcp__n8n_health_check (status ok, v2.48.3, https://n8n.lorettasercy.com)
  - Read N8N_API_KEY from User env via PowerShell [Environment]::GetEnvironmentVariable (267 chars, JWT iat 1777219215 / ~2026-04-26)
  - Same JWT is also configured in ~/.claude.json under mcpServers.n8n-mcp.env.N8N_API_KEY
  - Hit https://n8n.lorettasercy.com/api/v1/workflows with X-N8N-API-KEY header → HTTP 401 {"message":"unauthorized"} (Cloudflare-fronted)
  - Called mcp__n8n-mcp__n8n_list_workflows → AUTHENTICATION_ERROR (same key, same failure)
  - Added .env, .env.*, !.env.example to .gitignore
- What worked
  - MCP transport (stdio + npx n8n-mcp) and the tool registry — non-auth endpoints respond fine
  - Local env var plumbing — key is reachable from both the host and the MCP child process
- Blockers
  - n8n public REST API rejects the current JWT on both direct curl and MCP — key is stale/rotated server-side, not a header issue
  - Cannot verify 3.1 (r1pkTZ94DuuWrTtA) active state, cannot deploy or activate 2.4 until a fresh key is issued
  - Will not auto-read C:\Users\aserc\.lux\.env for a fresher key — standing CLAUDE.md rule requires asking first on .lux/credentials
- Next step
  - Alan: in n8n UI → Settings → API → rotate/copy a fresh API key, then `setx N8N_API_KEY "<new>"` and update ~/.claude.json mcpServers.n8n-mcp.env.N8N_API_KEY
  - On next session: re-run list_workflows, verify 3.1 active (activate via n8n_update_partial_workflow activateWorkflow op if not), then deploy 2.4 via n8n_create_workflow with PLACEHOLDER_GOOGLE_SHEETS swapped to sG8kOyb5bJb0hjgS on both Google Sheets nodes (success + error log), then activate 2.4
  - Pre-deploy reminder: also reconnect creds sG8kOyb5bJb0hjgS, xkF1H9p5Q52UPPoi, gbwzaRu0ONWfhuUr; set OPUS_CLIP_API_KEY / BUFFER_ACCESS_TOKEN / BUFFER_PROFILE_IDS env on the n8n VM; create "Video Log" tab in Sheet 1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM
