# Host — Infrastructure Reference

## Runtime Folder: C:\Users\aserc\.lux\
NOT in GitHub — credentials and runtime artifacts only.

### Key files
| File | Purpose |
|------|---------|
| `.env` | `ANTHROPIC_API_KEY` (suffix WwAA), `N8N_API_KEY` (suffix J2g), `VERITAS_SESSION_LOG_DOC_ID`, GCP vars |
| `google_client_secrets.json` | Drive OAuth client (host-side) |
| `google_oauth_token.json` | Drive OAuth token (host-side) |
| `drive_registry.json` | Canonical Drive asset IDs |
| `start_alan_os.bat` | Server launcher — use this to start alan_os_server.py |
| `ALAN_OS_HANDOFF.md` | Legacy handoff — superseded by Drive doc |
| `SESSION_A/B/C/STRATEGY.md` | Legacy session notes |
| `norman_inbox_guard.py` | Norman's AOL inbox triage — runs daily 6AM via Task Scheduler |
| `norman_inbox_sweep.py` | One-time sweep script |
| `norman_sender_audit.py` | Sender audit script |
| `norman_whitelist.txt` | 14 addresses + 2 domain rules (@penfed.org, @penfed.info) |
| `claude_usage_dashboard*.py/.html` | Claude token tracking — dormant by design (no admin key) |
| `claude_injector_v2.js` | Browser injection script |
| `triage_*_log.txt` (5 accounts) | Runtime logs — rotate freely |
| `loretta_dump*.txt` | Outlook inbox dumps for triage audits |
| `digest_log.txt` | Daily digest run log |

### Subfolders
| Folder | Purpose |
|--------|---------|
| `workflows/` | Python scripts, PS1 scripts, Task Scheduler XMLs — the working code layer |
| `Data/` | Runtime JSON: leads.json, competitors.json, tasks.json, ai_stack_feed.json, etc. |
| `Dashboard/` | React dashboard HTML served by alan_os_server.py |
| `backups/` | Workflow JSON snapshots |
| `credentials/` | gdocs_host_client.json, gdocs_host_token.json, service_account.json |
| `logs/` | norman_guard daily logs |
| `handoffs/` | current.md, archive |

---

## Code Layer: C:\Veritas\repos\alan-os\

### Server
- **alan_os_server.py** — FastAPI @ localhost:8000
- **Dashboard** — localhost:8000/dashboard (React, Phase 3 complete)
- **Quick Links panel** — 7 Drive assets, clickable cards
- **Task Scheduler:** `AlanOS_Server` task — auto-start at logon. XML at `~/.lux/workflows/AlanOS_Server_S4U.xml`

### Launcher — ALWAYS use this
- **lux_launcher.py** — `C:\Users\aserc\.lux\workflows\lux_launcher.py`
- Kills/restarts Outlook, sequences triage. NEVER run triage scripts directly.

### Triage scripts
| Script | Status | Account |
|--------|--------|---------|
| `triage.py` | ACTIVE | asercy@msn.com |
| `triage_gmail.py` | ACTIVE | alansercy@gmail.com |
| `triage_loretta_v2.py` | ACTIVE | lorettasercy@gmail.com |
| `triage_keys.py` | BACKBURNER | loretta.keysandcommunity@gmail.com (low volume) |
| `triage_mmm.py` | BACKBURNER | lsercy@mmmtrucks.com (low volume) |

### Known issues
| Script | Issue |
|--------|-------|
| `review_new_senders.py` | COM error — Loretta Gmail still syncing in Outlook. Fix: add Outlook kill/restart block |

### Drive sync
- **Script:** `scripts/post_closeout_to_drive.py`
- **Run at session close** — silent, token cached
- **Session Log Doc:** `1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38`

### GCP
- **Project:** lux-host-493415
- **Service account:** lux-automation@lux-host-493415.iam.gserviceaccount.com
- **Credentials:** `~/.lux/credentials/service_account.json`

### Drive Asset Registry
| Asset | Doc ID |
|-------|--------|
| Handoff Doc | `1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ` |
| Lux Command Center | `1hFOBfaKxBs1ZsP9hBfOXb17JZylScxkVRPpA6c0YWDc` |
| Job Search Brief | `1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ` |
| MMM Prospect Tracker | `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI` |
| NLM Inbox Feed folder | `1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN` |
| Loretta Content Calendar | `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM` |
| Veritas AI Research Feed | `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M` |
| Veritas Session Log | `1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38` |

---

## Key ENV Values
| Key | Value/Suffix | File |
|-----|-------------|------|
| ANTHROPIC_API_KEY | suffix WwAA | ~/.lux/.env |
| N8N_API_KEY | suffix J2g | ~/.lux/.env |
| VERITAS_SESSION_LOG_DOC_ID | 1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38 | ~/.lux/.env |
| GCP service account | — | ~/.lux/credentials/service_account.json |
| Google OAuth token | — | ~/.lux/credentials/gdocs_host_token.json |

---

## Open Infrastructure Items
| # | Item | Status |
|---|------|--------|
| 1 | n8n API key rotation | Manual — rotate in n8n UI (Settings → n8n API → Create new key) |
| 2 | MMM_SHEETS_URL missing from .env | Never re-added after repo init — find Apps Script deployment URL and add |
| 3 | Anthropic admin API key | Needed for authoritative Claude usage panel — create at console.anthropic.com/settings/admin-keys |
| 4 | WF4.1 writeback spot-check | Check MMM Prospect Tracker WA tab row 2 Notes field |
| 5 | Host :5678 listener | Unexpected — check `Get-NetTCPConnection -LocalPort 5678` |
