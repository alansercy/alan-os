# Alan OS — Master Project Registry
**Last Updated:** April 25, 2026
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
| Workflow 3.1 Gmail Triage | ✅ Live | Monitor for misclassifications |
| Workflow 3.2 Prospect Audit | ⏳ Blocked | Fix Google Sheets `__rl` node — Sheet ID: `1OePOK2GaGB2JrXO5QUSrXkzceGQ8V2l4` |
| Nimrat approval gate (3.1) | ⬜ Not started | Replace auto-send with draft-to-Nimrat flow |
| n8n auto-start Task Scheduler | ⬜ Not started | `schtasks /create /tn "n8n" /tr "npx n8n start" /sc onstart /ru SYSTEM` |
| HP Hood follow-up | 🔜 Deadline May 1 | Contact Matthew Bauer before May 1 re: full volume commitment |
| Stemilt/Gordy Schulze outreach | 🔜 Queued | Email Gordy for warm intro to Brendan — Food Shippers PS line |
| Second unpaid MMM client ($3K/mo) | ⏳ Blocked | Collection or renegotiation — unresolved |
| Workflow 2.3 Hot Lead SMS | ⬜ Not started | Lofty webhook → Twilio → Loretta |
| Workflow 2.4 Video Repurposing | ⬜ Not started | Edited video → Opus Clip → Reels → Buffer |

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
| 2.1 Weekly Content Brief | ✅ Live | Friction reduced Apr 26: Loretta sees 7 cols only (`Loretta Input View` filter on Content Calendar tab); `Default Status to Idea` Code node defaults blank Status so only Episode Title + Film Date are required to fire |
| 2.2 YouTube Description Generator | ✅ Live | Works but no auto-post |
| 2.5 UTM Slug Generator | ✅ Live | Works |
| Wave Report landing page `/the-wave1` | ✅ Live | Live but Loretta not using system |
| Auto-post to Instagram/YouTube | ⬜ Not built | Buffer/Publer selection pending |
| ManyChat comment triggers | ⬜ Not built | Phase 1: RELIST trigger only |
| PDF delivery automation | ⬜ Not built | Manual for Phase 1 |
| Lofty source tagging | ⬜ Not built | All leads land in one pile |
| Nurture sequences | ⬜ Not built | Phase 2 |

#### Rebuild Plan (per Infrastructure Brief Apr 25)
| Phase | Deliverable | Status |
|---|---|---|
| L1 | Reduce Sheet input to 2 fields | ✅ Apr 26 — Default Status node added to 2.1 (commit `912a6b9` in `loretta-os`); 10 cols hidden globally + `Loretta Input View` filter created (id `1704693960`) |
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
| Claude usage panel | ⏳ Blocked | `.env` currently holds a workspace key (`sk-ant-api03-...`), not an admin-scope key — admin endpoints will reject. Loader is BOM-tolerant (line 12). Needs true `sk-ant-admin-...` key in `ANTHROPIC_ADMIN_API_KEY`. |
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

---

### GitHub — Skills + Repo Foundation
| Repo | Status | Next Action |
|---|---|---|
| `apexbot` | ✅ v0.3 live | Session 3 picks up here |
| `alan-os` | ✅ Live | Repo live as of commit `bf88777` |
| `loretta-os` | ✅ Live | 5 n8n workflow JSON exports committed (Apr 26): 2.1, 2.2, 3.1, 3.2, AlanSercy MSN Flow. Keys scrubbed to `{{ANTHROPIC_API_KEY}}` placeholder. |
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
| ~~**A**~~ | ~~Governance~~ — ✅ Done Apr 25 (PROJECTS.md, Claude usage panel, loretta-os repo, cto.new note). Skill stubs deferred. | Host | — |
| **ApexBot S3** | Events.yaml, template capture, scheduler wiring, SVS test | Host | 60 min |
| **L1** | Loretta: reduce Sheet friction, wire Telegram → brief, Buffer auto-post | VM | 60 min |
| **L2** | Loretta: /relist-guide page, Lofty tagging, PDF delivery | VM | 90 min |
| **L3** | Loretta: ManyChat RELIST trigger, first nurture sequence | VM | 60 min |
| **W1** | Loretta: WordPress site build (Netlify, Roots & Room) | Host | 90 min |
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
