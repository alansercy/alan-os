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

## 2026-04-28 Concurrent Session — Rule Relax + Server Restart
- What was done
  - Per Alan this session, relaxed the CLAUDE.md credential/.lux confirmation rule (removed "Ask before any action that touches it" from line 18)
  - Read `.lux\.env` and confirmed `N8N_API_KEY` byte-for-byte matches the User env-var — no fresher key hiding there
  - Ran `schtasks /Run /TN AlanOS_Server`; task was already running, dashboard responds 200 on `/` (117 B) and `/dashboard` (28.5 KB)
  - This session's MCP boot did NOT include `mcp__n8n-mcp__*` tools — used REST directly. n8n-mcp registration is per-session.
- What worked
  - Independent confirmation of the 401 blocker (different MCP state, same outcome → key really is rotated server-side, not a transport issue)
- Blockers
  - Same n8n 401 — see entry above
- Next step
  - Same as above (Alan rotates the n8n API key); then `setx N8N_API_KEY` + update both `.lux\.env` and `~/.claude.json` so MCP and dashboard pick up the new value

## 2026-04-29 n8n Key Rotated — Auth Restored
- What was done
  - Read N8N_API_KEY from User env (new JWT, iat 1777470745 / 2026-04-29, ends `...ybaE`)
  - Verified ~/.claude.json `projects['C:/Veritas/repos/alan-os'].mcpServers.n8n-mcp.env.N8N_API_KEY` already holds the new key (matches env exactly)
  - Direct REST: `curl https://n8n.lorettasercy.com/api/v1/workflows` → HTTP 200, 15 workflows returned
  - **3.1 (r1pkTZ94DuuWrTtA) is ACTIVE** — no activation needed
  - Other live: 2.1, 2.2, 2.5, 2.6, C, AlanSercy MSN Flow, Daily Email Digest, AlanSercy Gmail, Telegram Callback Handler
  - Inactive: 2.3 (AukTldfaY4oWcu1Q), 2.4 not yet deployed, 3.2 (VvHYTjheeecJ441F currently inactive — was active during 04-28 live run, may need re-toggle), 2 stub workflows
- Blockers
  - Current MCP child process still has the old key in its spawn-time env (`mcp__n8n-mcp__n8n_list_workflows` still returns AUTHENTICATION_ERROR). File-side fix is correct; needs Claude Code session restart to refresh the MCP env.
  - 2.4 deploy not executed this turn — defer to next session so MCP can do it cleanly via `n8n_create_workflow` rather than raw REST POST
- Incident note
  - First attempt to update ~/.claude.json via PowerShell pipeline used `ConvertFrom-Json -Depth 100`, which doesn't exist in PS5.1 — pipeline produced empty `$json`, my `WriteAllText` zeroed the file. Restored from `.claude.json.bak-20260429` (taken pre-mutation, 30385 B). Backup since deleted. Pre-write backup is now the standing pattern for any mutation of `.claude.json`.
- Next step
  - Restart Claude Code so n8n-mcp respawns with new env; then run `n8n_list_workflows` → expect success
  - Then deploy 2.4: `n8n_create_workflow` from `workflows/workflow_2_4_video_repurposing.json` with PLACEHOLDER_GOOGLE_SHEETS → `sG8kOyb5bJb0hjgS` on both Sheets nodes; activate via partial-update
  - Also worth re-checking 3.2 active state — it shows inactive on the wire, may need a UI toggle
