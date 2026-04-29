# Alan OS — Master Project Registry
**Last Updated:** April 29, 2026 (Workflow 2.4 deployed + active, MMM Gmail cred reauthed, n8n-mcp + memory bank live)
**Owner:** Alan Sercy | CentPenny LLC / Veritas AI Partners
**Canonical location:** GitHub → `alan-os` repo → `PROJECTS.md`
**Session protocol:** See `SESSION_PROTOCOL.md` for the canonical open/close flow across claude.ai and Claude Code. Templates in `templates/`. Legacy: paste this file URL into Claude at session start + state environment (Host/VM) + objective.

---

## HOW TO USE THIS FILE
- This is the single source of truth for all active projects
- Update it at the END of every session via `push_handoff.py` or manual commit
- Claude reads this at session START — do not reconstruct from memory
- Status legend: ✅ Done | 🔨 Active | ⏳ Blocked | 🔜 Queued | ⬜ Not started

---

## RECENTLY COMPLETED — April 29, 2026

| Item | Result | Reference |
|---|---|---|
| MMM-fix — Gmail cred reauth | ✅ Done | Cred `68RydHz0N1dUAj9S` reconnected; 3.1 active, 3.2 ready to fire |
| Workflow 2.4 — Video Repurposing deploy | ✅ Done — active in n8n | ID `tX09Uxf9LdjVLmvl`; webhook `https://n8n.lorettasercy.com/webhook/video-repurpose` |
| n8n-mcp + n8n-skills install | ✅ Done | Commit `97af608` |
| Memory bank — initialized | ✅ Done | Commit `97af608` (`memory-bank/session-log.md` + CLAUDE.md protocol) |
| Lux Command Center — Phase 3 | ✅ Done | Commit `a55f9a2` |

**Blocked / Waiting:**
- **Workflow 2.4 end-to-end test** — waiting on `OPUS_CLIP_API_KEY` + `BUFFER_ACCESS_TOKEN` + `BUFFER_PROFILE_IDS` (set on n8n VM env) + Loretta recording the source video. Workflow itself is deployed and active; first real run cannot fire until these four prerequisites land.

---

## TIER 1 — REVENUE GENERATING (Act Now)

### MMM Trucking Automation
**Entity:** CentPenny LLC | **Retainer:** $3K/mo active
**Environment:** VM (n8n localhost:5678)
| Item | Status | Next Action |
|---|---|---|
| Workflow 3.1 Gmail Triage | ✅ Active | Gmail OAuth cred `68RydHz0N1dUAj9S` reauthed Apr 29; workflow `r1pkTZ94DuuWrTtA` confirmed active. Hourly runs resumed. |
| Workflow 3.2 Prospect Audit | 🔜 Ready to fire | Sheet ID fixed Apr 26 (`1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI`, versionId `2c1fb3d1-84b0-4498-81f0-28b29d91451b`). Cred reauth done Apr 29. **Next:** click Execute on `VvHYTjheeecJ441F` for end-to-end audit; consider re-toggling active. Backup at `C:\Users\aserc\.lux\workflows\3_2_backup_pre_patch.json`. |
| Nimrat approval gate (3.1) | ⬜ Not started | Replace auto-send with draft-to-Nimrat flow |
| n8n auto-start Task Scheduler | 🔨 Scripts staged Apr 26 | Two PS1 scripts at `handoff/vm-scripts/` ready to paste into elevated PowerShell on VM: `01_register_n8n_autostart.ps1` (Task Scheduler entry) + `02_add_mmm_sheets_url.ps1` (writes corrected sheet ID to `.n8n\.env`). n8n filesystem writes are blocked everywhere on VM, so deploy is manual paste — see scripts in repo |
| HP Hood follow-up | 🔜 Deadline May 1 | Contact Matthew Bauer before May 1 re: full volume commitment |
| Stemilt/Gordy Schulze outreach | 🔜 Queued | Email Gordy for warm intro to Brendan — Food Shippers PS line |
| Second unpaid MMM client ($3K/mo) | ⏳ Blocked | Collection or renegotiation — unresolved |
| Workflow 2.3 Hot Lead SMS | 🔨 Skeleton built Apr 26 | Created inactive at id `AukTldfaY4oWcu1Q` — Gmail trigger on MMM inbox → reply filter → Claude classify → IF hot/warm → Twilio SMS + Gmail backup. **Blocked on:** Twilio credential (acct SID + auth token + from-number) and Loretta's mobile (E.164). Placeholders `__SET_LORETTA_MOBILE_E164__` / `__SET_TWILIO_FROM_E164__` / `__SET_TWILIO_CRED_ID__` in node "SMS Loretta". Note: trigger reuses dead Gmail cred, so will inherit 3.1's blocker |
| Workflow 2.4 Video Repurposing | ✅ Deployed + active Apr 29 | n8n ID `tX09Uxf9LdjVLmvl`. Webhook: `https://n8n.lorettasercy.com/webhook/video-repurpose`. Sheets nodes wired to cred `sG8kOyb5bJb0hjgS`. **End-to-end test waiting on:** `OPUS_CLIP_API_KEY` / `BUFFER_ACCESS_TOKEN` / `BUFFER_PROFILE_IDS` env on n8n VM + Loretta source video. See Workflow 2.4 detail subsection below. |

**Key contacts:** Nimrat Samra (CEO, lsercy@mmmtrucks.com) | Matthew Bauer (HP Hood) | Gordy Schulze (Stemilt)
**Sheets:** MMM Prospect Tracker `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI`

#### Workflow 2.4 detail (deployed Apr 29)

**Status:** DEPLOYED + ACTIVE — End-to-End Test Waiting on Env Vars + Source Video

**Deploy facts:**
- n8n workflow ID: `tX09Uxf9LdjVLmvl`
- Webhook URL: `https://n8n.lorettasercy.com/webhook/video-repurpose` (POST)
- Manual trigger also wired (n8n UI Execute Workflow)
- Both Google Sheets nodes (Log Success, Log Error) use cred `sG8kOyb5bJb0hjgS`
- Validator: 0 errors, 29 non-blocking warnings (typeVersion bumps + cosmetic)
- Source JSON: `workflows/workflow_2_4_video_repurposing.json`
- Notes: `workflows/workflow_2_4_notes.md`

**Pending — first real run blocked on (4 items):**
1. **`OPUS_CLIP_API_KEY`** — set in n8n VM env (Settings → Environment). Source: https://opus.pro → Settings → API.
2. **`BUFFER_ACCESS_TOKEN`** — set in n8n VM env. Source: Buffer developer dashboard OAuth token.
3. **`BUFFER_PROFILE_IDS`** — set in n8n VM env. Comma-separated Buffer profile IDs for Loretta's accounts.
4. **Loretta source video** — Loretta records and provides the first MP4 URL. Send via webhook POST `{video_url, video_title, platforms}`.

**Also confirm before first run:**
- `Video Log` tab exists in Content Calendar `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM` with columns `Date | Video Title | Clips Generated | Platforms | Status | Buffer Response | Submitted At`.

**Validator-flagged future polish (optional, non-blocking):**
- Bump typeVersions: Webhook 2→2.1, HTTP Request 4.2→4.4, IF 2→2.3, Google Sheets 4.4→4.7
- Add `cachedResultName` on Sheets RL fields so the n8n UI shows the resource name
- Add `onError` handlers to HTTP / Sheets / Webhook nodes
- Tag the workflow `loretta` / `video` / `content` in the n8n UI (MCP tag-add op currently errors on this instance)

---

### Veritas AI Partners — Digital Presence Clients
**Entity:** CentPenny LLC / Veritas AI Partners
| Item | Status | Next Action |
|---|---|---|
| Painter client website | 🔨 Active | Demo tomorrow — confirm scope, build SOW |
| Health enthusiast website | 🔜 Queued | Scope TBD after painter demo |
| Veritas Offer Sheet template | ⬜ Not started | Build after painter SOW — extract reusable pattern |
| Veritas positioning paragraph | ⬜ Not started | 3 variants: fractional exec / AI-leveraged BD / TBD |
| DBA filing — Rockwall County | ⬜ Not started | Assumed Name Certificate — CentPenny LLC |
| **cto.new pipeline evaluation** | 🔍 Evaluating | Test workflow: cto.new generates polished scaffold → import to GitHub → Claude Code customizes and wires backend → Netlify or cto.new hosts → user owns everything. Use painter site as first trial. Compare against direct Claude Code build for speed/quality/cost. |

---

### Job Search — Resume & Outbound System
**Status:** 🔨 In Progress
**Target:** W2/1099 CRO or EVP BD roles (remote) | **Runway:** ~5 months
**Canonical assets:** `C:\Veritas\assets\veritas\resume\` (planned post-reorg location)
**Master resume Drive ID:** *(to be added after upload)*

**Completed:**
- Resume v2 built (Veritas brand, two-column, headshot, AI callout)
- Cover letter exists (needs full rewrite)

**Next actions (in order):**
1. Fill placeholders — LinkedIn URL, Rocktop numbers, Citi years/title
2. Add "Earlier Career — Citigroup/CitiMortgage" condensed line
3. Rewrite cover letter — AI-native operator angle, no generic language
4. Build Workflow 4 — resume auto-tailoring (master resume → role-specific version via Claude)
5. Build Workflow 5 — outbound tracker Google Sheet
6. Confirm Workflow 1 (job email scoring) and NotebookLM push are active
7. Push resume to Drive canonical location, share link

#### General job search items
| Item | Status | Next Action |
|---|---|---|
| Job Search Brief | ✅ Live | Drive: `1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ` |
| NLM Stage 2 job review workflow | ⬜ Not started | Build review/score/act pipeline — 10 jobs pending; queue file: `C:\Users\aserc\.lux\Data\pending_jobs.json` |
| Rocktop/TSI/Mercury outreach | ⬜ Not started | 3 messages drafted but not sent |
| EPR dedup logic | ⬜ Not started | EPR queued 3x in `pending_jobs.json`; reset script: `C:\Users\aserc\.lux\workflows\reset_job_search_dedup.py` |

---

## TIER 2 — FOUNDATION (Build Right)

### ApexBot — Evony Automation
**Repo:** github.com/alansercy/apexbot (private) | **Version:** v0.3
**Environment:** Host machine (Windows PC)
| Item | Status | Next Action |
|---|---|---|
| core/planner.py full build | ✅ Session 2 | — |
| modules/gathering.py | ✅ Session 2 | Needs template capture before live run |
| modules/march_coordinator.py | ✅ Session 2 | Needs wiring into scheduler |
| tools/capture_template.py | ✅ Session 2 | — |
| spec/events.yaml SVS/KE flags | ⬜ Session 3 | Add march_block + gather_caution flags |
| vision/templates/ | ⬜ Session 3 | Template capture: gather_button, march_button, close_popup |
| scheduler.py wiring | ⬜ Session 3 | Register march_coordinator for 4 alts |
| modules/rallies.py | ⬜ Session 3+ | Stub then build |
| SVS status | ⏳ ACTIVE | All marches blocked — flip flag after SVS ends (est. Apr 30) |
| RageBot expiry | ⏳ Apr 30 | Market entry window open — BlueStacks Nougat32 broken |

**ADB:** `C:\ProgramData\Rage Systems\Ragebot\Android\platform-tools\adb.exe`
**Ports:** 5555 | 5595 | 5605 | 5625 | 5645

---

### Loretta — MoveWithClarity Content Engine
**Environment:** VM (n8n) + Host (Python triage)
**Brand:** Roots & Room — Charcoal/Sage Forest/Fresh Sage | DM Serif Display / DM Sans
**Headshot:** `cdn.lofty.com/image/fs/user-info/2026121/15/w600_original_329b765f-5c29-4c1a-9ce8-d6498e92a6c0-jpeg.webp`

#### Current System (honest audit)
| Workflow | Status | Problem |
|---|---|---|
| 2.1 Weekly Content Brief | ⏳ OAuth blocked | Friction reduced Apr 26: Loretta sees 7 cols only (`Loretta Input View` filter on Content Calendar tab); `Default Status to Idea` Code node defaults blank Status so only Episode Title + Film Date are required to fire. **Now blocked on Google Sheets/Docs OAuth re-auth — see queue below.** |
| 2.2 YouTube Description Generator | ⏳ OAuth blocked | Works when creds valid; blocked on Google Sheets/Docs re-auth |
| 2.5 UTM Slug Generator | ⏳ OAuth blocked | Trigger cred + Sheets cred both revoked |
| 2.6 Content Intake Form | ⏳ OAuth blocked | Trigger cred + Sheets cred both revoked |
| C — Loretta Telegram Topic Intake | 🔨 Active, end-to-end tested Apr 26 PM | Workflow `q0aogZju1nET96kP`. Webhook URL `https://unaltered-stiffly-renewably.ngrok-free.dev/webhook/loretta-topic-intake`. Append to Content Calendar verified via exec `13476`. Telegram bot still needs `setWebhook` call to start receiving Loretta's real messages |
| Wave Report landing page `/the-wave1` | ✅ Live | Live but Loretta not using system |
| Auto-post to Instagram/YouTube | ⬜ Not built | Buffer/Publer selection pending |
| ManyChat comment triggers | ⬜ Not built | Phase 1: RELIST trigger only |
| PDF delivery automation | ⬜ Not built | Manual for Phase 1 |
| Lofty source tagging | ⬜ Not built | All leads land in one pile |
| Nurture sequences | ⬜ Not built | Phase 2 |

**OAuth re-auth queue (Apr 2026):** Three Google creds revoked refresh tokens around Apr 12–14. Re-auth must happen in the n8n web UI (Credentials → click cred → Reconnect → complete Google consent). Public REST API cannot perform the OAuth handshake.

**Apr 26 PM update:** Re-auth attempted, hit `redirect_uri_mismatch`. n8n's redirect URI is `https://unaltered-stiffly-renewably.ngrok-free.dev/rest/oauth2-credential/callback` — must be added to the Google OAuth client's "Authorized redirect URIs" in GCP Console → APIs & Services → Credentials. To find the right OAuth client: open the n8n credential edit form (Client ID is plaintext), or capture from Network tab during a "Sign in with Google" click. Workflow C's append-to-Sheet *did* succeed in test exec `13476`, suggesting `sG8kOyb5bJb0hjgS` may be partially functional — verification needed after browser re-auth completes.

⚠️ **ngrok URL rotates on every restart**, breaking redirect URIs. Switch to a paid ngrok static subdomain or Cloudflare Tunnel before any further re-auth work.

| Cred ID | Name | Blocks | Apr 26 PM status |
|---|---|---|---|
| `sG8kOyb5bJb0hjgS` | Google Sheets account | 2.1, 2.2, 2.5, 2.6, C, 3.2, 2.4 | Append works (exec 13476); reads/triggers unverified |
| `xkF1H9p5Q52UPPoi` | Google Sheets Trigger account | 2.5, 2.6 (trigger nodes) | Still failing |
| `gbwzaRu0ONWfhuUr` | Google Docs account | 2.1, 2.2 | Unverified |

**Note:** `CONTEXT.json` `workflows.needs_reauth` mirrors these three IDs as of Apr 28.

#### Rebuild Plan (per Infrastructure Brief Apr 25)
| Phase | Deliverable | Status |
|---|---|---|
| L1 | Reduce Sheet input to 2 fields | ✅ Apr 26 — Default Status node added to 2.1 (commit `912a6b9` in `loretta-os`); 10 cols hidden globally + `Loretta Input View` filter created (id `1704693960`) |
| L1 | Telegram → Sheet topic intake (Workflow C) | ✅ Apr 26 PM — built, debugged, end-to-end verified (loretta-os: `4a597f0` initial build + `2efbf53` debug fixes). Three issues fixed: telegramTrigger swapped to regular webhook (auto-registration silently failing); Parse Topic reads `$json.body.message`; append needs `columns.schema`. Webhook live at `https://unaltered-stiffly-renewably.ngrok-free.dev/webhook/loretta-topic-intake` |
| L1 | Wire Buffer auto-post | ⬜ Queued — L1 remainder |
| L1 | `/relist-guide` landing page (Phase 1 per brief) | ⬜ Session L2 |
| L2 | Lofty source tagging — 8 tags configured | ⬜ Session L2 |
| L2 | PDF delivery automation via Lofty | ⬜ Session L2 |
| L2 | ManyChat RELIST trigger | ⬜ Session L3 |
| L2 | First nurture sequence (4 emails, Relist-specific) | ⬜ Session L3 |
| L3 | Remaining guide pages (New Build, Land Trap, Divorce) | ⬜ After L2 |

**Guide content status:**
- ✅ Content complete: Relist Guide, New Build Guide, Land Buyer Trap, Divorce Guide
- ⬜ Pending: Parents Move, Before You Leave Suburbs, Seller Protection
- 📋 Wave Report pillars: Built by Alan, do not change architecture

**WordPress migration:** Queued for Session W1 — build on Netlify, Roots & Room brand

---

### Lollie & Lovie Lou — Children's Book Brand
**Owner:** Loretta Sercy (Alan supports operations)
**Environment:** Host | **URL:** lollieandlovielou.com (live)

| Item | Status | Next Action |
|---|---|---|
| Website (index.html + resource-guide.html) | ✅ Live | Mobile review — flag layout issues |
| 4-book series — A Day Full of Wonders / Lovie Lou Can / Breathing with Lovie Lou / Goodnight Lovie Lou | 🔨 Active | Build audience first, self-publish Book 1 via Amazon KDP + IngramSpark |
| Google Workspace email | ⏳ Pending | $7/mo Starter — loretta@ + hello@ alias; TXT verification in Netlify DNS panel |
| Printful merch setup | ⏳ Pending | Create Printful account, build 6 Canva designs, order samples, activate Shop tab |
| Etsy / Shopify storefront | ⬜ Not started | Linked from Shop tab — Etsy free or Shopify Starter $5/mo |
| Social handles (@lollieandlovielou) | ⬜ Not started | Secure on Instagram / TikTok / Facebook |
| Resource guide signups (Netlify Forms) | ✅ Live | Monitor at app.netlify.com → lolliewebsitefinal → Forms |

**Strategy doc:** `strategy/lollie_brand.md`
**Subject / photo approval:** Brielle (granddaughter, autism Level 2) — Gabi (Brielle's mom) approves all photos

---

### Alan OS — Dashboard + Automation Infrastructure
**Environment:** Host | `localhost:8000/dashboard`
**Start:** `C:\Users\aserc\.lux\start_alan_os.bat`
**Server:** `C:\Users\aserc\.lux\workflows\alan_os_server.py`

| Item | Status | Next Action |
|---|---|---|
| Dashboard live | ✅ Live | Evolving — needs Claude usage panel |
| Daily digest email | ✅ Live | 8:05 AM, includes command center |
| Email triage — 5 accounts | ✅ Live | MSN, Gmail, Loretta, Keys, MMM |
| Drive integration — 6 assets | ✅ Live | Service account: `lux-automation@lux-host-493415.iam.gserviceaccount.com` |
| Claude usage panel | ⏳ Blocked on admin key | `.env` currently holds a workspace key (`sk-ant-api03-...`), not an admin-scope key — admin endpoints will reject. Loader is BOM-tolerant (line 12). Needs true `sk-ant-admin01-...` key in `ANTHROPIC_ADMIN_API_KEY` — see "Admin API key" below for creation steps. |
| Push handoff to Drive | ✅ Live | `push_handoff.py` |
| Task Scheduler (alan_os_server) | ⬜ Not started | Add auto-start at login |
| Obsidian install + setup | ⬜ Queued | Scoped, not installed |
| Dashboard Drive Panel UI | ⬜ Not started | New tab showing registered asset cards |
| Sunday evening weekly preview | ⬜ Queued | — |
| Attachment harvester | ⬜ Queued | PDFs from known senders → folders |

**Claude Usage Setup follow-ups (Apr 25–26, 2026 session):**
1. ✅ **Workspace key rotation** — Apr 26: leaked `sk-ant-api03-s1gFMM...` / `XaB_iH...` / `pzDMW...` revoked; fresh workspace key in `ANTHROPIC_API_KEY`; n8n state patched across 5 workflows (6 node-parameter occurrences) via `/api/v1/workflows/{id}` PUT and verified clean.
2. **Create real admin-scope key for dashboard** — current `.env` value is a workspace key, not admin. Console → API Keys → Create Key → select **Admin** scope (requires org-admin role). Add as `ANTHROPIC_ADMIN_API_KEY=sk-ant-admin-...` to `.env`.
3. **Re-add `MMM_SHEETS_URL` to `.env`** — `outbound_campaign.py` had a hardcoded Apps Script deployment URL; it was scrubbed during the lux-os repo init. Uncomment line 4 of `.env` and paste the URL back, otherwise the script can't reach the prospect tracker.
4. **Identify AlanSercy MSN Flow purpose** — n8n workflow ID `7GEpqCGS2cP0J8wY` surfaced during the rotation (no Anthropic key, so just bystander). Likely part of the 5-account email triage stack. Confirm whether it's redundant with the Python `triage.py` scripts in `lux-os/workflows/` or doing something different.

#### Admin API key (manual creation required)
Anthropic admin-scope keys (`sk-ant-admin01-...`) cannot be minted via API — they must be created interactively by an org-admin. This is the single blocker for the Claude usage panel.

1. Open https://console.anthropic.com/settings/admin-keys (must be signed in as an Organization Admin — not just a workspace member).
2. Click **Create Key** → name it e.g. `alan-os-dashboard-admin` → confirm.
3. Copy the `sk-ant-admin01-...` value (it is shown once only).
4. On host: append to `C:\Users\aserc\.lux\.env`:
   ```
   ANTHROPIC_ADMIN_API_KEY=sk-ant-admin01-...
   ```
5. Restart `start_alan_os.bat` and the Claude usage panel should populate.

**Scope:** Admin keys can read org-wide usage/cost across all workspaces and projects, and manage workspaces/members/keys. Treat as a higher-trust secret than workspace keys — never commit, never paste into n8n nodes.

---

### GitHub — Skills + Repo Foundation
| Repo | Status | Next Action |
|---|---|---|
| `apexbot` | ✅ v0.3 live | Session 3 picks up here |
| `alan-os` | ✅ Live | Repo live as of commit `bf88777` |
| `loretta-os` | ✅ Live | 8 n8n workflow JSON exports committed (latest `4a597f0` Apr 26): 2.1, 2.2, 2.5, 2.6, 3.1, 3.2, AlanSercy MSN Flow, C (Telegram intake). Keys scrubbed to `{{ANTHROPIC_API_KEY}}` placeholder. README documents OAuth re-auth queue. |
| `lux-os` | ✅ Live | 75 files (workflows, dashboards, Norman guard); secrets gitignored; `outbound_campaign.py` needs `MMM_SHEETS_URL` re-added to `.env` |
| `caveman` | ⚠️ SKILL.md written | Commit to GitHub |
| `codeburn` | ⚠️ Stub only | Populate SKILL.md next session |
| `design-extract` | ⚠️ Stub only | Populate SKILL.md next session |
| NLM Skills Library notebook | ⬜ Not created | Add Caveman/Codeburn/Design as source docs |

**Session start protocol (GitHub not yet connected):**
- Claude Code: `cd C:\[repo]` then `claude` — direct filesystem + git access, no copy-paste
- claude.ai: paste PROJECTS.md URL for cross-project strategy sessions
- GitHub MCP: not available in registry yet — check periodically

---

## TIER 3 — FAMILY + PERSONAL

### Estate Planning — Norman & Marsha Sercy
| Item | Status | Next Action |
|---|---|---|
| Charles property — structural resolution | ⏳ Active | Title vesting, loan obligations, probate exposure |
| Charles communication strategy | ⏳ Active | Await parents' reaction before next move |
| Estate Planning CC doc | ⬜ Pending | Drive ID pending — add to drive_registry.json |
| USAA claim management | 🔨 Active | 7 open items (down from 11) |
| Endurance warranty claim (Dominick) | 🔨 Active | 5 items complete, Indiana DOI closed |

### Family Property Hit List
| Item | Status | Next Action |
|---|---|---|
| 3275 CR 26100, Roxton TX (Tumminello) | ⏳ Active | Waiting signed buyer rep + People's Bank confirmation |

### Norman Inbox Guard
**Account:** sercypete@aol.com (Norman's AOL) | **Environment:** Host
**Schedule:** Daily 6AM via Task Scheduler — "Norman Inbox Guard"

| Item | Status | Next Action |
|---|---|---|
| Inbox triage script | ✅ Live | `C:\Users\aserc\.lux\norman_inbox_guard.py` |
| Daily digest to Alan | ✅ Live | 6AM to alansercy@gmail.com |
| Whitelist | ✅ Live | `C:\Users\aserc\.lux\norman_whitelist.txt` — 14 addresses + 2 domain rules (@penfed.org, @penfed.info) |
| USAA auto-routing | ✅ Live | Routes to Inbox/USAA folder |
| Forwarding to Marsha (sercymarsha@aol.com) | ⏳ Staged | Set `FORWARDING_ENABLED = True` in script when ready |
| `review_new_senders.py` COM error | ⏳ Blocked | "Exhausted shared resources" — root cause: Loretta Gmail background-syncing in Outlook; fix: Outlook kill/restart + wait for sync before re-test |

**SOP:** `sops/lux_stack.md`
**Logs:** `C:\Users\aserc\.lux\logs\norman_guard_YYYY-MM-DD.log`

---

## ORCHESTRATION ENGINE

| Component | Status | Notes |
|---|---|---|
| ORCH-1 (`orchestrator.py`)   | ✅ Live | Sequential agent execution; reads `DIRECTIVE.md`, decomposes via Claude Code, runs agents one at a time. |
| ORCH-2 (`orchestrator_v2.py`) | ✅ Built and merged to `main` | Parallel execution via `ThreadPoolExecutor`. Two-wave model: `can_run_parallel: true` agents run concurrently, then sequential agents. Imports v1 helpers — no v1 changes. See `ORCH-2-SPEC.md`. |
| `CONTEXT.json` | ✅ Updated v1.1 | Real system state: owner, clients (MMM Trucking, Veritas), Drive registry, people, product stack, job-search status, standing rules. `needs_reauth` carries real n8n cred IDs (`sG8kOyb5bJb0hjgS`, `xkF1H9p5Q52UPPoi`, `gbwzaRu0ONWfhuUr`) as of Apr 28. |
| Agents | ✅ Defined | `agents/agent_a.md`, `agents/agent_b.md`, `agents/agent_c.md` |

---

## LIVE INFRASTRUCTURE

| Component | Status | Notes |
|---|---|---|
| Session Protocol | ✅ COMPLETE (Apr 28) | `SESSION_PROTOCOL.md` defines how every session opens and closes across both surfaces (claude.ai and Claude Code). Templates in `templates/`: `HANDOFF_TEMPLATE.md` (manual fill-in for claude.ai close), `session_close.md` (paste into Claude Code to produce `SESSION_NOTES.md`), `session_start.md` (paste into new claude.ai chat to resume). Setup note: `<GITHUB_RAW_PROJECTS_URL>` placeholder in `session_start.md` must be filled in once a GitHub remote is configured. |

---

## COMMUNICATION LAYER

### Telegram Bots (both live)
| Bot | Owner | Use |
|---|---|---|
| Alan's bot | alansercy@gmail.com | Urgent alerts, n8n notifications |
| Loretta's bot | lorettasercy@gmail.com | **Content trigger** — type topic → auto-generates brief + queues post |

**Loretta Telegram workflow (to build Session L1):**
Loretta texts topic → n8n webhook → Claude generates brief + caption + hashtags → Buffer schedules → Sheet auto-updated as record

### ManyChat (to configure)
| Trigger | Guide | Status |
|---|---|---|
| RELIST | /relist-guide | ⬜ Phase 1 |
| NEW BUILD | /new-build-guide | ⬜ Phase 2 |
| LAND | /land-buyer-trap | ⬜ Phase 2 |
| SURVIVE | /divorce-guide | ⬜ Phase 2 |
| PARENTS | /parents-move-guide | ⬜ Phase 3 |
| SUBURBS | /before-you-leave-the-suburbs | ⬜ Phase 3 |
| SELLER | /seller-protection-guide | ⬜ Phase 3 |
| WAVE | /the-wave1 | ⬜ Phase 2 |

---

## DRIVE ASSET REGISTRY

| Asset | Account | Doc ID |
|---|---|---|
| Handoff Doc | alansercy@gmail.com | `1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ` |
| Lux Command Center | alansercy@gmail.com | `1hFOBfaKxBs1ZsP9hBfOXb17JZylScxkVRPpA6c0YWDc` |
| Job Search Brief | alansercy@gmail.com | `1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ` |
| MMM Prospect Tracker | lsercy@mmmtrucks.com | `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI` |
| Loretta Content Calendar | lorettasercy@gmail.com | `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM` |
| Veritas AI Research Feed | alansercy@gmail.com | `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M` |
| NLM Inbox Feed folder | alansercy@gmail.com | `1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN` |

---

## SESSION QUEUE — NEXT SESSIONS IN ORDER

| Session | Focus | Environment | Est. Time |
|---|---|---|---|
| ~~**A**~~ | ~~Governance~~ — ✅ Done Apr 25 | Host | — |
| ~~**MMM-fix**~~ | ~~Gmail cred reauth~~ — ✅ Done Apr 29. Cred `68RydHz0N1dUAj9S` reconnected; 3.1 active. Remaining sub-step: click Execute on `VvHYTjheeecJ441F` to verify 3.2 audit emails. | VM | — |
| **2.3-finish** | After Twilio account exists: store credential in n8n, fill `__SET_*__` placeholders in workflow `AukTldfaY4oWcu1Q`, activate. Need Loretta's mobile in E.164 | VM | 15 min |
| ~~**2.4-deploy**~~ | ~~Deploy + activate Workflow 2.4~~ — ✅ Done Apr 29 (ID `tX09Uxf9LdjVLmvl`). E2E test waiting on `OPUS_CLIP_API_KEY` / `BUFFER_ACCESS_TOKEN` / `BUFFER_PROFILE_IDS` env on VM + Loretta source video. | VM | — |
| **ApexBot S3** | Events.yaml, template capture, scheduler wiring, SVS test | Host | 60 min |
| **L1** | Loretta: reduce Sheet friction, wire Telegram → brief, Buffer auto-post | VM | 60 min |
| **L2** | Loretta: /relist-guide page, Lofty tagging, PDF delivery | VM | 90 min |
| **L3** | Loretta: ManyChat RELIST trigger, first nurture sequence | VM | 60 min |
| **W1** | Loretta: WordPress site build (Netlify, Roots & Room) | Host | 90 min |
| **MMM** | Chief of Staff Proposal — needs context dump from Alan | Host | 45 min |
| **Veritas** | Painter SOW (after demo), health enthusiast SOW | Host | 45 min |
| **GitHub** | alan-os repo, loretta-os repo, skill stubs populated | Host | 60 min |
| **VIE** | Veritas Intelligence Engine — V1: Workflow 5.1 (inbox → URL extract → Claude enrich → `ai_stack_feed.json` → dashboard panel). Full spec in ROADMAP section below. Ready to spec next session, no blockers. | Host | 90 min |

---

## STANDING REMINDERS
- Trash: Every Thursday 8pm (Friday pickup)
- Recycle: Every other Tuesday 8pm (Wednesday pickup 4pm CST) — next: Wed Apr 29
- HP Hood deadline: May 1 — Matthew Bauer contact
- ApexBot SVS ends: est. Apr 30 — flip `active_override: false` in events.yaml
- RageBot expiry: Apr 30 — market entry window

---

## EXPANDED PROJECT DOCUMENTATION (Apr 28, 2026)

This section captures canonical detail for projects whose at-a-glance status sits in the TIER tables above. Reference here for "what is this and what's the next move"; reference the TIER tables for "is anything active right now."

### Alan OS Dashboard

**Status:** Phases 1–4 complete | Phases 5–6 queued

- **Server:** `C:\Users\aserc\.lux\workflows\alan_os_server.py`
- **Dashboard URL:** `localhost:8000/dashboard`
- **React UI:** `C:\Users\aserc\.lux\dashboard\index.html`
- **Task Scheduler:** live (auto-start configured)
- **Drive integration:** live (GCP project `lux-host-493415`, service account `lux-automation@lux-host-493415.iam.gserviceaccount.com`)
- **Phases queued:**
  - Phase 5 — Knowledge hub
  - Phase 6 — Family stewardship + vault

### NLM Intelligence Loop

**Status:** Live (last confirmed run April 20, 2026)

- **Engine:** `nlm_feed_builder.py` v1.4 at `C:\Users\aserc\.lux\workflows\`
- **Notebooks (5):**
  - AI Stack Intelligence
  - Job Search Qualified
  - Veritas AI Partners
  - Real Estate AI
  - MMM Trucking
- **Pipeline:** Two-stage job search scoring
- **Task Scheduler status:** unknown — needs verification

**Next action:** Verify Task Scheduler entry is active and has been running since Apr 20.

### Job Search OS

**Status:** Partial — Workflows 1 and 2 built; 3 and 4 not yet built

- **Workflow 1** — Job email scoring | built, active status unknown
- **Workflow 2** — NLM push | built, active status unknown
- **Workflow 3** — Resume tailoring (master → role-specific via Claude) | not built
- **Workflow 4** — Outbound tracker Google Sheet | not built
- **Master resume:** rebuilt today — `C:\Veritas\assets\veritas\resume\AlanSercy_Resume_Veritas_2025.docx`

**Next action:** Confirm Workflows 1 and 2 active in n8n once the Loretta Sheets/Docs cred reauth lands; then build Workflow 3 (resume tailoring).

### ApexBot

**Status:** Sessions 1–2 complete | Session 3 pending | RageBot subscription concern

- **Repo:** `github.com/alansercy/apexbot` (private) — local at `C:\Veritas\repos\apexbot`
- **BlueStacks instances (5):** ports `5555 / 5595 / 5605 / 5625 / 5645`
- **ADB path:** `C:\ProgramData\Rage Systems\Ragebot\Android\platform-tools\adb.exe`
- **RageBot subscription:** may have lapsed — was expiring April 30, 2026. Verify before Session 3.

### Lollie & Lovie Lou

**Status:** Live — site, email, and brand assets in place

- **Live site:** `lollieandlovielou.com` (Netlify)
- **Email:** `loretta@lollieandlovielou.com` (Google Workspace)
- **Built assets:** pitch deck, one-pager, submission package — at `C:\Veritas\assets\lovie-and-lollie\`
- **Not yet:**
  - **Series Bible** — character canon, story arc for the 4-book series, brand guardrails
  - **Publisher targets** — named list of houses to query

### Norman Inbox Guard

**Status:** Live — daily 6AM digest to Marsha

- **Script location:** `C:\Users\aserc\.lux\workflows\` (per Apr 28 inventory). Existing TIER 3 entry references the file at `C:\Users\aserc\.lux\norman_inbox_guard.py` — verify whether the canonical path is `.lux\` root or `.lux\workflows\` before any future edits.
- **Schedule:** Daily 6AM via Task Scheduler ("Norman Inbox Guard")
- **Whitelist:** `C:\Users\aserc\.lux\norman_whitelist.txt` (14 addresses + 2 domain rules)

### Barn Conversion

**Status:** Planning

- **Building:** 30×40 metal building
- **Budget ceiling:** $75K
- **Layout:** locked
- **HVAC:** locked — Mitsubishi `MXZ-3C36NA` (3-zone outdoor unit)

**Next action:** Exit planning into spec / contractor selection.

### Dominick / Endurance Warranty Claim

**Status:** Active — Indiana DOI regulator tracker live

- **Tracker:** Indiana Department of Insurance regulator
- **Subject:** Endurance warranty claim, Dominick (Norman & Marsha vehicle)
- **Note (potential conflict to reconcile):** the Estate Planning TIER 3 row above states "Indiana DOI closed." This expanded entry says the regulator tracker is active and ongoing. Verify whether a new/separate complaint is now open or whether the TIER 3 row is stale.

---

## ROADMAP — PLANNED OS COMPONENTS (Apr 28, 2026)

### ORCH-3 — Agent-to-Agent Triggering

**Status:** Planned
**Priority:** High — unlocks fully autonomous pipeline

**Description:**
Extend ORCH-2's parallel execution engine to support automatic agent handoffs. When one workflow completes and meets defined criteria, it triggers the next agent without human intervention.

**First two targets:**
1. Workflow 3.2 prospect audit finds a gap → automatically triggers outbound sequencing agent.
2. Deal marked closed in MMM tracker → automatically triggers Operations agent to generate onboarding SOP.

**Depends on:** ORCH-2 (complete), Google Sheets webhook or polling layer.

**Next action:** Design handoff contract spec — what data passes between agents, what conditions trigger the next agent, what happens on failure.

### FinanceOS

**Status:** Backburner — do not touch yet
**Priority:** Highest long-term moat

**Description:**
AI finance agent handling nightly transaction reconciliation, revenue tracking, financial reporting, and commission calculations.

**First client (planned):** Veritas / MMM revenue stack — $6K/mo MMM + $18K catch-up + Stemilt pipeline.

**Architecture needs (deferred):** bank/transaction data source, Google Sheets or Quickbooks integration, nightly Claude API call for categorization and anomaly detection, morning summary report to Alan.

**Blocker:** Needs dedicated architecture session before any build.

**Canonical note:** Biggest commercial moat in the stack. Do not start until MMM and digital presence revenue is stable and the job search is resolved.

**Next action:** Schedule architecture session — inputs, outputs, data sources, privacy model, report format.

### Alan Sercy — LinkedIn Authority Track

**Status:** Not started
**Priority:** High — feeds Veritas BD pipeline and job search simultaneously

**Description:**
B2B personal brand content engine on LinkedIn targeting PE-backed operators, startup founders, and SMB owners who need AI revenue infrastructure. Separate from Loretta's real estate content. Alan's voice: 28-year revenue executive who builds and deploys AI ops systems — not a tech vendor, a trusted advisor.

**Target audience:**
- PE-backed company operators (Series A–C)
- Startup founders needing first CRO / revenue infrastructure
- SMB owners in financial services, trucking, real estate adjacent
- Executive recruiters and hiring managers at AI-native companies

**Content pillars (3):**
1. **Revenue operations war stories** — 28 years of closes, turnarounds, lessons. Human, specific, no fluff.
2. **AI in the field** — what actually works deploying for real clients (MMM, AgentOS, real results, no hype).
3. **Executive perspective on AI** — where the market is going, what operators get wrong, what to build vs buy.

**Posting cadence:** 3× per week minimum once launched.
**Format priority:** Short-form text first (highest LinkedIn reach), video repurposing second once content rhythm is established.

**Dependencies:**
- Resume finalized (in progress — see Job Search OS)
- LinkedIn profile updated to match new Veritas positioning
- First 10 posts drafted before going live (content buffer)

**Workflow to build (Phase 2):**
- n8n **Workflow 5** — LinkedIn post scheduler from content brief
- Claude drafts posts from Alan's voice guide
- Alan reviews and approves before publish
- Performance tracking in Google Sheet

**Voice guide (to be written — session task):**
Direct, warm, and earned. Lead with the specific and earn the general. Never thought-leadership clichés. Never "AI is transforming everything." Always: here is what I did, here is what happened, here is what it means for you.

**Canonical assets:** `C:\Veritas\assets\veritas\linkedin\`

**Next action:** Update LinkedIn profile headline and About section to reflect Veritas AI Partners positioning. Draft first 3 posts.

### Veritas AI Partners — Product Waitlist Pages

**Status:** Not started
**Priority:** High — captures inbound while products are built

**Description:**
Single landing page per OS vertical capturing waitlist signups. No full site needed yet. One page per product: clear one-sentence value proposition, 3 bullets on what it does, email capture form. Goes live BEFORE the LinkedIn authority track launches so traffic has a destination.

**Pages to build (in order):**
1. **AgentOS** — "AI revenue operations for real estate agents. Find more leads, follow up automatically, close faster."
2. **TradeOS** — "AI business development for trucking, HVAC, plumbing, and trades. Your pipeline runs while you work."
3. **PersonalOS** — "AI life operations for executives and family stewards. Your life runs like a business."

**Tech stack:**
- Single HTML file per product (one Claude Code session each)
- Veritas brand kit: Navy `#0B1E3D`, Gold `#C6A96A`, DM Sans + Cormorant Garamond
- Email capture via Netlify Forms (free, no backend)
- Subdomains:
  - `agentos.veritasaipartners.com`
  - `tradeos.veritasaipartners.com`
  - `personalos.veritasaipartners.com`

**MMP validation rule:**
Each page goes live BEFORE full product build begins. <10 signups in 30 days → do not build that vertical. ≥10 signups → green light to build. **Exception:** AgentOS already deployed for MMM — use as social proof on the page.

**Waitlist email sequence (3 emails, Claude drafts):**
1. **Confirmation** — "You're on the list. Here's what we're building."
2. **Week 2** — "Here's a real result from our current client."
3. **Launch** — "Early access is open. Here's your invite."

**Canonical assets:** `C:\Veritas\assets\veritas\waitlist-pages\`
**Depends on:** LinkedIn authority track (traffic source), Veritas domain DNS access (subdomain setup).

**Next action:** Build AgentOS waitlist page first — one Claude Code session, deploy to Netlify same day.

**Strategic note:** This is the MMP validation gate. No more building OS verticals without a waitlist signal first.

### Veritas Intelligence Engine (VIE)

**Status:** Queued — ready to spec
**Priority:** High — eliminates manual research loop; sellable component inside PersonalOS and AgentOS

**Description:**
Autonomous AI research radar. Monitors email inbox for AI/tool links, enriches each via Claude (summarize, evaluate fit, relevance score), stores in `ai_stack_feed.json`, surfaces ranked recommendations on the dashboard. The goal is to replace the manual "save link, read later, evaluate" loop with a continuously-running pipeline that pre-digests and ranks new inputs before Alan ever sees them.

**Versioning:**
- **V1 — email only.** Inbox is the single source. Proves the enrichment + ranking + surface loop end-to-end.
- **V2 — multi-source fan-in.** Same enrichment pipeline, additional inputs: GitHub trending, RSS feeds, X/Twitter saves, Reddit subscriptions. All converge on `ai_stack_feed.json`.

**First build — Workflow 5.1:**
1. Trigger: scheduled scan of inbox (Gmail OAuth via existing creds)
2. Extract: URLs from email bodies + subject lines
3. Enrich: HTTP Request to Anthropic per CLAUDE.md §2 (typeVersion 4.2, `x-api-key`, raw body) — Claude summarizes, scores relevance, evaluates fit against Veritas/AgentOS/PersonalOS pipelines
4. Store: append enriched record to `C:\Users\aserc\.lux\data\ai_stack_feed.json`
5. Surface: dashboard panel with ranked recommendations + filter by pipeline/score

**Why it matters:**
- Eliminates manual research loop (Alan's current bottleneck on AI tool tracking)
- Sellable component inside PersonalOS and AgentOS — every executive client has the same problem
- Reuses the SalesOS pattern (wrapped JSON file + FastAPI endpoint + dashboard panel) — low marginal cost to ship

**Blocker:** None. Ready to spec next session.

**Next action:** Draft Workflow 5.1 spec to `docs/workflow_5_1_spec.md` (mirror the structure of `workflow_4_1_spec.md`); add `ai_stack_feed.json` schema + `GET /ai_stack`, `POST /ai_stack` endpoints to `alan_os_server.py` (mirror `/leads` pattern).

---
*Generated: April 25, 2026 — End of cross-project governance session*
*Last updated: April 29, 2026 — Workflow 2.4 deployed + active (`tX09Uxf9LdjVLmvl`), MMM Gmail cred reauthed, n8n-mcp + memory bank live, all three Google creds confirmed green*
*Next update: push via `push_handoff.py` or `git commit` at end of next session*
