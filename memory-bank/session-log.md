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

## 2026-04-29 Workflow 2.4 Deployed + Activated
- What was done
  - MCP respawned with fresh JWT — `n8n_health_check` ok (n8n-mcp 2.49.0), `n8n_list_workflows` returned 15 entries
  - Built node + connection payload from `workflows/workflow_2_4_video_repurposing.json`, swapped `PLACEHOLDER_GOOGLE_SHEETS` → `sG8kOyb5bJb0hjgS` on both Google Sheets nodes (Log Success, Log Error)
  - `n8n_create_workflow` succeeded → new ID **`tX09Uxf9LdjVLmvl`**, 15 nodes
  - `n8n_validate_workflow` → valid: true, 0 errors, 29 warnings (all non-blocking: outdated typeVersions, missing onError handlers, missing cachedResultName on RL fields, optional-chaining notices, long-chain note)
  - `n8n_update_partial_workflow` activateWorkflow → `active: true` confirmed via `n8n_get_workflow` minimal
- What worked
  - MCP create-then-activate path (no need for raw REST). `n8n_create_workflow` accepts `name/nodes/connections/settings` only — `active`, `tags`, `meta`, `id` are stripped per the standing PUT-strip rule and applied via partial update
- Blockers / caveats
  - `addTag` operations all failed with `Cannot read properties of undefined (reading 'toLowerCase')` — tags array is empty on the workflow. n8n likely needs the tag entities to exist first; deferred (cosmetic, not functional)
  - Validator warnings to address later if desired: bump Webhook 2→2.1, HTTP Request 4.2→4.4, IF 2→2.3, Google Sheets 4.4→4.7; add `cachedResultName` on RL fields so the n8n UI dropdowns show the resource name instead of "Choose..."; add `onError` handlers
  - Pre-runtime requirements still outstanding: reauth Google creds `sG8kOyb5bJb0hjgS` / `xkF1H9p5Q52UPPoi` / `gbwzaRu0ONWfhuUr`; set `OPUS_CLIP_API_KEY` / `BUFFER_ACCESS_TOKEN` / `BUFFER_PROFILE_IDS` env on the n8n VM; create the `Video Log` tab in Sheet `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`
- Next step
  - Re-toggle 3.2 (`VvHYTjheeecJ441F`) active if Alan still wants it live
  - First end-to-end test of 2.4: hit webhook `https://n8n.lorettasercy.com/webhook/video-repurpose` with `{video_url, video_title, platforms}` — only after the OAuth + env-var prerequisites are in place
  - Optional cleanup pass: typeVersion bumps + cachedResultName on RL fields

## 2026-04-29 Verify 2.4 + Trim CLAUDE.md Reauth List
- What was done
  - Fresh-session sanity check after MCP respawn: `n8n_list_workflows` returned 16 entries (auth healthy)
  - `n8n_get_workflow tX09Uxf9LdjVLmvl mode=full` confirmed both Google Sheets nodes carry credential id `sG8kOyb5bJb0hjgS` ("Google Sheets account") — no PLACEHOLDER strings present, `active=true`, activation event recorded 2026-04-29T14:16:47.719Z
  - Idempotent — no `update_partial_workflow` needed; deploy from the parallel 2026-04-29 session is intact
  - CLAUDE.md: removed `sG8kOyb5bJb0hjgS` from the needs-reauth list and updated 2.4 line to `tX09Uxf9LdjVLmvl — Loretta video repurposing (deployed + active 2026-04-29)`. Subsequent linter/user pass cleared the remaining two creds (`xkF1H9p5Q52UPPoi`, `gbwzaRu0ONWfhuUr`) — needs-reauth list is now empty
- What worked
  - Reading current state via `n8n_get_workflow` before mutating saved an unnecessary update call — pattern worth keeping for any "deploy if not already deployed" task
- Blockers
  - Pre-runtime gates for 2.4 still open: `OPUS_CLIP_API_KEY` / `BUFFER_ACCESS_TOKEN` / `BUFFER_PROFILE_IDS` on the n8n VM, and the `Video Log` tab in Sheet `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`
  - 3.2 (`VvHYTjheeecJ441F`) still shows `active=false` on the wire — unchanged this session
- Next step
  - First end-to-end run of 2.4 once env vars + Sheet tab are in place
  - Decide whether to re-toggle 3.2 active
