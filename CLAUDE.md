# CLAUDE.md — Alan OS Master State
**Last updated:** 2026-05-03
**Updated by:** Session G

---

## HOW TO USE THIS FILE

This is the first file every session reads. It answers three questions before touching anything:
1. What is built and confirmed working?
2. What is open and who owns it?
3. What must never be touched?

At session close, update the MASTER STATE section before committing. No exceptions.
Session protocol: read this file → execute directive → update this file → commit → push.

---

## OPERATOR CONTEXT

Alan Sercy — 33-year revenue executive, founder Veritas AI Partners (CentPenny LLC DBA).
Active W2/1099 job search targeting CRO/EVP BD at PE-backed or AI-driven companies (remote only).
Runway: ~5 months. MMM Trucking generating income.

Environments:
- Host: C:\Users\aserc\ — Alan OS, personal automation, MMM, parents, inbox triage
- VM: SecureAI-W11 — Veritas productized code, n8n workflows
- All repos: C:\Veritas\repos\

Key accounts: asercy@msn.com · alansercy@gmail.com · lorettasercy@gmail.com · loretta.keysandcommunity@gmail.com · lsercy@mmmtrucks.com

---

## MASTER STATE

### INFRASTRUCTURE

| Component | Status | Location | Notes |
|-----------|--------|----------|-------|
| alan_os_server.py | RUNNING | ~/.lux/workflows/alan_os_server.py | FastAPI on localhost:8000 |
| Dashboard | LIVE | localhost:8000/dashboard → ~/.lux/Dashboard/index.html | Active dashboard |
| Quick Links panel | LIVE | Dashboard nav "Quick Links" | 7 Drive assets, clickable cards |
| Drive sync | RUNNING | scripts/post_closeout_to_drive.py | Silent, token cached 4/30 |
| Task Scheduler | SET | AlanOS_Server task in Windows Scheduler | S4U XML at ~/.lux/workflows/AlanOS_Server_S4U.xml |
| lux_launcher.py | WORKING | ~/.lux/workflows/lux_launcher.py | Kills/restarts Outlook, sequences triage |
| Triage — MSN | WORKING | triage.py | |
| Triage — Gmail | WORKING | triage_gmail.py | |
| Triage — Loretta | WORKING | triage_loretta_v2.py | Inbox cleaned to 23 legit emails |
| Triage — Keys | BACKBURNER | | Low volume, deprioritized |
| Triage — MMM | BACKBURNER | | Low volume, deprioritized |
| review_new_senders.py | COM ERROR | | Loretta Gmail still syncing — fix: Outlook kill/restart block |
| n8n Workflow 4.1 | DEPLOYED | ID: zl9peS1ZGNISLibZ | API key rotation needed for live test |
| GCP service account | LIVE | project: lux-host-493415 | lux-automation@lux-host-493415.iam.gserviceaccount.com |
| NotebookLM loop | ACTIVE | 4 notebooks under alansercy@gmail.com | AI Fundamentals · Automation · Job Search · Real Estate AI |
| claude_usage_dashboard.py | DORMANT | | Needs Anthropic admin API key — not set, dormant by design |

### REPO STATE

| Repo | HEAD | Branch | Location |
|------|------|--------|----------|
| alan-os | d9d059a | main | C:\Veritas\repos\alan-os |
| loretta-os | — | main | C:\Veritas\repos\loretta-os |
| apexbot | — | — | C:\Veritas\repos\apexbot |
| memory-bank | — | — | C:\Veritas\repos\memory-bank |

### KEY ENV VALUES

| Key | Value/Suffix | File |
|-----|-------------|------|
| ANTHROPIC_API_KEY | suffix WwAA | ~/.lux/.env |
| N8N_API_KEY | suffix J2g | ~/.lux/.env |
| VERITAS_SESSION_LOG_DOC_ID | 1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38 | ~/.lux/.env |
| GCP service account | — | ~/.lux/credentials/service_account.json |
| Google OAuth token | — | ~/.lux/credentials/gdocs_host_token.json |

### DRIVE ASSET REGISTRY

| Asset | Doc ID |
|-------|--------|
| Handoff Doc | 1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ |
| Lux Command Center | 1hFOBfaKxBs1ZsP9hBfOXb17JZylScxkVRPpA6c0YWDc |
| Job Search Brief | 1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ |
| MMM Prospect Tracker | 1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI |
| NLM Inbox Feed folder | 1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN |
| Loretta Content Calendar | 1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM |
| Veritas AI Research Feed | 1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M |
| Veritas Session Log | 1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38 |

---

## VERITAS PRODUCT MAP

| Product | Vertical | Proof of Concept | Status |
|---------|----------|-----------------|--------|
| AgentOS | Real estate agents + SMB revenue | Loretta eXp operation | Live POC, no waitlist page |
| TradeOS | Skilled trades: HVAC, electrical, plumbing, painting, lawn care | SanMiguel Painting Co | First live client deployed |
| SalesOS | Field sales, BD, outbound pipeline | Alan OS + MMM Trucking | Architecture specced, not built |
| PersonalOS | Executives, family stewards | Alan OS | Live POC, no waitlist page |
| FinanceOS | PROTECTED | — | DO NOT TOUCH |

Waitlist rule: 10 signups before any product build.
Public surface: None yet. LinkedIn live 5/3/2026. No waitlist pages, no Veritas website.
SanMiguel live URL: https://ephemeral-cajeta-5fd460.netlify.app
Brand: Navy #0B1E3D / Gold #C6A96A
Tagline formal: "Simplifying Matters. Setting the Standard."
Tagline signature: "Simplifying Matters. Where Table Stakes End."

---

## OPEN ITEMS

| # | Item | Blocker | Owner |
|---|------|---------|-------|
| 1 | Job Search Brief 1PyDF update | LinkedIn live — ready | Claude Code |
| 2 | n8n API key rotation | Manual — rotate in n8n UI | Alan |
| 3 | WF4.1 writeback spot-check | MMM Prospect Tracker WA tab row 2 check Notes | Alan |
| 4 | Netlify site rename | Optional cosmetic | Alan |
| 5 | Gmail OAuth redirect_uri_mismatch | Google Cloud Console fix | Alan |
| 6 | Veritas waitlist pages | Need domain decision first | Planning |
| 7 | Veritas website | No domain yet | Planning |
| 8 | VERITAS_BRAND_KIT.md | Not written yet | This chat |
| 9 | SalesOS architecture build | After waitlist rule met | Queued |
| 10 | Ruflo content post | LinkedIn live — ready to write | This chat |

---

## REQUIRED CONTEXT FILES

Read these before any session that touches the relevant area:
- docs/veritas-company-narrative.md — Veritas positioning, products, brand
- SESSION_NOTES.md — current session state
- CLOSEOUT.md — session closeout template
- docs/closeout_sync_spec.md — Drive sync spec (STATUS: COMPLETE)
- PROJECTS.md — active project registry

---

## SESSION CLOSE PROTOCOL

Before every commit, Claude Code must:
1. Mark completed tasks done in tasks.json
2. Update MASTER STATE section in this file with current status
3. Update SESSION_NOTES.md
4. Run python scripts/post_closeout_to_drive.py
5. Confirm working tree clean
6. Commit and push

---

## DO NOT REVISIT

| Item | Closed | Notes |
|------|--------|-------|
| VIE Steps 1-4 + OAuth/Drive | 4/30/2026 | Token cached, script running silently |
| HP Hood | Closed | Do not resurface |
| Loretta brand kit / DESIGN.md | Done | Do not rebuild |
| Workflow 4.1 import | Done | ID zl9peS1ZGNISLibZ |
| tasks 013-020 | Closed | All done |
| post_closeout_to_drive.py | Complete | Runs silently |
| 8081 mystery | Resolved | claude_usage_dashboard.py dormant by design |
| lux-os as separate repo | Resolved | Does not exist — all work in alan-os |

---

## STANDING REMINDERS

- Trash: Thursday 8pm (Friday pickup)
- Recycle: Every other Tuesday 8pm (Wednesday 4pm pickup)
- Bulk pickup: First Friday of month (put out Thursday night)
