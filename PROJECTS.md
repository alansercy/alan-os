# Alan OS — Master Project Registry
**Last Updated:** April 26, 2026 (evening session — n8n autonomous fixes)
**Owner:** Alan Sercy | CentPenny LLC / Veritas AI Partners
**Canonical location:** GitHub → `alan-os` repo → `PROJECTS.md`
**Session protocol:** Paste this file URL into Claude at session start + state environment (Host/VM) + objective

---

## HOW TO USE THIS FILE
- This is the single source of truth for all active projects
- Update it at the END of every session via `push_handoff.py` or manual commit
- Claude reads this at session START — do not reconstruct from memory
- Status legend: ✅ Done | 🔨 Active | ⏳ Blocked | 🔜 Queued | ⬜ Not started

---

## TIER 1 — REVENUE GENERATING (Act Now)

### MMM Trucking Automation
**Entity:** CentPenny LLC | **Retainer:** $3K/mo active
**Environment:** VM (n8n localhost:5678)
| Item | Status | Next Action |
|---|---|---|
| Workflow 3.1 Gmail Triage | ⏳ Blocked | **Was silently broken since Apr 13** — Gmail OAuth cred `68RydHz0N1dUAj9S` (MMM Trucking) refresh token revoked, every 2-hour run errored. Re-auth in n8n UI: Credentials → MMM Trucking → Reconnect |
| Workflow 3.2 Prospect Audit | ⏳ Blocked on Gmail re-auth | Sheet ID **fixed Apr 26** — was `1OePOK2GaGB2JrXO5QUSrXkzceGQ8V2l4` (a Doc, not a Sheet); patched to `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI` (versionId `2c1fb3d1-84b0-4498-81f0-28b29d91451b`). Backup: `C:\Users\aserc\.lux\workflows\3_2_backup_pre_patch.json`. After 3.1 cred re-auth, click Execute on `VvHYTjheeecJ441F` to fire end-to-end test |
| Nimrat approval gate (3.1) | ⬜ Not started | Replace auto-send with draft-to-Nimrat flow |
| n8n auto-start Task Scheduler | 🔨 Scripts staged Apr 26 | Two PS1 scripts at `handoff/vm-scripts/` ready to paste into elevated PowerShell on VM: `01_register_n8n_autostart.ps1` (Task Scheduler entry) + `02_add_mmm_sheets_url.ps1` (writes corrected sheet ID to `.n8n\.env`). n8n filesystem writes are blocked everywhere on VM, so deploy is manual paste — see scripts in repo |
| HP Hood follow-up | 🔜 Deadline May 1 | Contact Matthew Bauer before May 1 re: full volume commitment |
| Stemilt/Gordy Schulze outreach | 🔜 Queued | Email Gordy for warm intro to Brendan — Food Shippers PS line |
| Second unpaid MMM client ($3K/mo) | ⏳ Blocked | Collection or renegotiation — unresolved |
| Workflow 2.3 Hot Lead SMS | 🔨 Skeleton built Apr 26 | Created inactive at id `AukTldfaY4oWcu1Q` — Gmail trigger on MMM inbox → reply filter → Claude classify → IF hot/warm → Twilio SMS + Gmail backup. **Blocked on:** Twilio credential (acct SID + auth token + from-number) and Loretta's mobile (E.164). Placeholders `__SET_LORETTA_MOBILE_E164__` / `__SET_TWILIO_FROM_E164__` / `__SET_TWILIO_CRED_ID__` in node "SMS Loretta". Note: trigger reuses dead Gmail cred, so will inherit 3.1's blocker |
| Workflow 2.4 Video Repurposing | 📋 Scoped Apr 26 | Memo at `strategy/workflow_2_4_video_repurposing_scope.md`. Opus Clip API is public (1 credit = 1 min, 30 req/min, webhook callbacks). **Pre-build asks for Loretta:** Opus Clip plan tier (does it include API?), Buffer plan tier, approval-gate preference (auto-post vs review) |

**Key contacts:** Nimrat Samra (CEO, lsercy@mmmtrucks.com) | Matthew Bauer (HP Hood) | Gordy Schulze (Stemilt)
**Sheets:** MMM Prospect Tracker `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI`

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

### Job Search
**Target:** W2/1099 CRO or EVP BD roles (remote) | **Runway:** ~5 months
| Item | Status | Next Action |
|---|---|---|
| Job Search Brief | ✅ Live | Drive: `1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ` |
| NLM Stage 2 job review workflow | ⬜ Not started | Build review/score/act pipeline — 10 jobs pending |
| Rocktop/TSI/Mercury outreach | ⬜ Not started | 3 messages drafted but not sent |
| EPR dedup logic | ⬜ Not started | EPR queued 3x in pending_jobs.json |

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
| `sG8kOyb5bJb0hjgS` | Google Sheets account | 2.1, 2.2, 2.5, 2.6, C, 3.2 | Append works (exec 13476); reads/triggers unverified |
| `xkF1H9p5Q52UPPoi` | Google Sheets Trigger account | 2.5, 2.6 (trigger nodes) | Still failing |
| `gbwzaRu0ONWfhuUr` | Google Docs account | 2.1, 2.2 | Unverified |

#### Rebuild Plan (per Infrastructure Brief Apr 25)
| Phase | Deliverable | Status |
|---|---|---|
| L1 | Reduce Sheet input to 2 fields | ✅ Apr 26 — Default Status node added to 2.1 (commit `912a6b9` in `loretta-os`); 10 cols hidden globally + `Loretta Input View` filter created (id `1704693960`) |
| L1 | Telegram → Sheet topic intake (Workflow C) | ✅ Apr 26 PM — built, debugged, end-to-end verified (loretta-os commit `4a597f0` + follow-up). Three issues fixed: telegramTrigger swapped to regular webhook (auto-registration silently failing); Parse Topic reads `$json.body.message`; append needs `columns.schema` |
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
| Loretta Content Calendar | lorettasercy@gmail.com | `1D7krpNO3CmuZCWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM` # VERIFY: B or C after muZ — check against Drive before using in automation |
| Veritas AI Research Feed | alansercy@gmail.com | `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M` |
| NLM Inbox Feed folder | alansercy@gmail.com | `1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN` |

---

## SESSION QUEUE — NEXT SESSIONS IN ORDER

| Session | Focus | Environment | Est. Time |
|---|---|---|---|
| ~~**A**~~ | ~~Governance~~ — ✅ Done Apr 25 | Host | — |
| **MMM-fix** | **🔥 First** — Re-auth Gmail cred `68RydHz0N1dUAj9S` in n8n UI, then run vm-scripts/01 + 02 in elevated PS on VM, then click Execute on workflow `VvHYTjheeecJ441F` to verify 3.2 audit emails Loretta. After that, 3.1 should resume hourly success | VM | 20 min |
| **2.3-finish** | After Twilio account exists: store credential in n8n, fill `__SET_*__` placeholders in workflow `AukTldfaY4oWcu1Q`, activate. Need Loretta's mobile in E.164 | VM | 15 min |
| **ApexBot S3** | Events.yaml, template capture, scheduler wiring, SVS test | Host | 60 min |
| **L1** | Loretta: reduce Sheet friction, wire Telegram → brief, Buffer auto-post | VM | 60 min |
| **L2** | Loretta: /relist-guide page, Lofty tagging, PDF delivery | VM | 90 min |
| **L3** | Loretta: ManyChat RELIST trigger, first nurture sequence | VM | 60 min |
| **W1** | Loretta: WordPress site build (Netlify, Roots & Room) | Host | 90 min |
| **2.4-build** | After Loretta confirms Opus Clip + Buffer plan tiers and approval-gate preference, build per `strategy/workflow_2_4_video_repurposing_scope.md` | VM | 4–6 hr |
| **MMM** | Chief of Staff Proposal — needs context dump from Alan | Host | 45 min |
| **Veritas** | Painter SOW (after demo), health enthusiast SOW | Host | 45 min |
| **GitHub** | alan-os repo, loretta-os repo, skill stubs populated | Host | 60 min |

---

## STANDING REMINDERS
- Trash: Every Thursday 8pm (Friday pickup)
- Recycle: Every other Tuesday 8pm (Wednesday pickup 4pm CST) — next: Wed Apr 29
- HP Hood deadline: May 1 — Matthew Bauer contact
- ApexBot SVS ends: est. Apr 30 — flip `active_override: false` in events.yaml
- RageBot expiry: Apr 30 — market entry window

---
*Generated: April 25, 2026 — End of cross-project governance session*
*Next update: push via `push_handoff.py` or `git commit` at end of next session*
