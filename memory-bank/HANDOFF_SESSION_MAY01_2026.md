# SESSION HANDOFF — May 1, 2026
**Repo:** `C:\Veritas\repos\alan-os`
**Dashboard:** `localhost:8081` (Lux Command Center)
**FastAPI:** `localhost:8000` (auto-starts on logon via Task Scheduler)
**n8n:** `https://n8n.lorettasercy.com`
**Last committed:** `9b99cf3` (Workflow 4.1 built), `46d059a` (3.2 active-toggle retired)

---

## WHAT SHIPPED THIS SPRINT (Apr 29–30 + May 1)

### Alan OS
- ✅ FastAPI server auto-starts on logon (Task Scheduler)
- ✅ VIE Step 4 — AI Stack tab live on Lux Command Center
- ✅ SalesOS tab live on Lux Command Center — leads + competitors panels, all three pipeline filters
- ✅ `/leads` GET/POST/PATCH, `/leads/pipeline`, `/competitors` endpoints — live
- ✅ `leads.json` and `competitors.json` — clean (test data wiped)
- ✅ n8n API key rotated — new JWT in `~/.lux/.env`
- ✅ GSD installed globally — `get-shit-done-cc@latest` (99 packages, v1.39.0-rc.4)
  - 65 skills → `~/.claude/skills/`
  - SDK dist landed in npm global prefix, NOT `~/.claude/sdk/dist/cli.js`
  - `/gsd-*` commands installed but may error on first invoke — test `/gsd-help` to confirm
  - Fix if broken: symlink npm global dist to expected path (Claude Code will know how)

### Workflows
- ✅ Workflow 3.1 — MMM Gmail Triage (active)
- ✅ Workflow 3.2 — MMM Prospect Audit (active, manual trigger)
- ✅ Workflow 4.1 — Lead Enrichment — **BUILT + COMMITTED (`9b99cf3`), NOT YET DEPLOYED**

### Loretta Brand (this session — web chat, not Claude Code)
- ✅ North Star positioning locked: Slate & Fog color system, DM Serif Display + DM Sans
- ✅ `movewithclarity_brandkit_slate.html` — full brand kit built
- ✅ `loretta_blueprint_final.html` — seller presentation, Slate & Fog
- ✅ `loretta_template_base.html` — base template for all future builds
- ✅ `LORETTA_BRAND.md` — canonical brand reference file
- ✅ `lorettasercy_homepage_slate.html` — homepage rebuilt on Slate & Fog, North Star copy applied
- ✅ All files at: `C:\Veritas\assets\loretta\`

---

## WHAT IS BLOCKED / NOT YET DONE

### Workflow 4.1 — Three steps to go live

**Blocker A — Gmail cred ID**
`PLACEHOLDER_GMAIL` at line 423 of `workflow_4_1_lead_enrichment.json` needs real cred ID.
Confirmed by Alan: `jFnLpO3jTd8SKeBR` = `alansercy@gmail.com` (Gmail account, created 2026-03-22).
**Action:** Patch `PLACEHOLDER_GMAIL` → `jFnLpO3jTd8SKeBR`, commit.

**Blocker B — Cloudflare Tunnel (replaces ngrok)**
Decision made: Use Cloudflare Tunnel (free, permanent) instead of ngrok.
Target public URL: `api.veritasaipartners.com` → `localhost:8000`
Setup commands (one-time, on host machine):
```
winget install cloudflare.cloudflared
cloudflared tunnel login
cloudflared tunnel create veritas-hub
cloudflared tunnel route dns veritas-hub api.veritasaipartners.com
cloudflared tunnel run veritas-hub
```
Add `cloudflared tunnel run veritas-hub` to Task Scheduler (same as alan_os_server.py).
Set env var: `ALAN_OS_PUBLIC_URL=https://api.veritasaipartners.com`
**Action:** Claude Code sets up Cloudflare Tunnel, adds to Task Scheduler, sets env var.

**Blocker C — n8n import + activate**
Once A + B are done:
- Import `workflows/workflow_4_1_lead_enrichment.json` via n8n UI at `https://n8n.lorettasercy.com`
- Activate workflow
- Test: POST `{"lead_id":"1"}` (Stemilt Growers)
- Confirm lead appears in Lux SalesOS tab under `mmm_trucking → prospect`

### Workflow 4.1 Scope Correction
Loretta RE pipeline is **Lofty-managed** — Lofty is system of record for `loretta_re`.
Do NOT wire loretta_re leads into `leads.json` or SalesOS.
Workflow 4.1 scope = `mmm_trucking` + `veritas_bd` pipelines only.
Update workflow JSON and notes accordingly.

### Loretta Capture Workflows (4.2 + 4.3) — NOT STARTED
Spec lives at: `C:\Veritas\assets\loretta\CLAUDE_CODE_SESSION_SALESOS_LORETTA.md`
**NOTE:** `loretta_re` inbound capture via alan-os is deprioritized — Lofty handles it.
4.2 and 4.3 may be deferred or repurposed for Veritas BD / lollieandlovielou inbound.
Revisit after Cloudflare Tunnel is live and 4.1 is deployed.

### GSD SDK path fix
Test `/gsd-help` in Claude Code. If it errors:
```
Find npm global prefix: npm prefix -g
Symlink: mklink /D "%USERPROFILE%\.claude\sdk" "<npm-global-prefix>\node_modules\get-shit-done-cc\sdk"
```

### VIE Steps remaining
- Step 2: Augment `nlm_feed_builder.py` with `extract_ai_stack_urls()`, enrichment prompt, POST to `/ai_stack`
- Step 3: OAuth client setup, create "Veritas Session Log" Google Doc, set `VERITAS_SESSION_LOG_DOC_ID` in `.env`
- Step 5: Run `nlm_feed_builder.py` against real AI-research email

### Loretta Website — Next builds
All on `loretta_template_base.html`. WordPress-ready semantic HTML.
Pages to build:
- `/sell` — Blueprint as web page + CTA
- `/buy` — buyer guide + transition framing
- `/transitions` — North Star positioning page
- `/resources` — gated hub (New Build Guide, Wave Report, net sheet)
Wave Report landing page needs visual rebrand to Slate & Fog (currently navy/gold wrong system).

### Net Sheet Calculator
Standalone tool — `/net-sheet`. Sale price + mortgage + costs → net proceeds.
One Claude Code session. Build after Loretta pages.

---

## PIPELINE / LEAD STATE

| Pipeline | System of record | SalesOS role | Current leads |
|---|---|---|---|
| `loretta_re` | Lofty CRM | Monitor only — do not duplicate | 0 in leads.json |
| `mmm_trucking` | leads.json | Full pipeline, SalesOS canonical | 0 (test data wiped) |
| `veritas_bd` | leads.json | Full pipeline, SalesOS canonical | 0 (test data wiped) |

MMM active: HP Hood fully closed (never surface as open). Gordy/Stemilt test underway.

---

## INFRASTRUCTURE STATE

| Component | Status | Notes |
|---|---|---|
| `alan_os_server.py` | ✅ Running | Auto-starts, port 8000 |
| `lux_launcher.py` | ✅ Live | Never run individual triage scripts directly |
| n8n | ✅ Running | `https://n8n.lorettasercy.com` |
| Cloudflare Tunnel | ❌ Not set up | Priority next session |
| `ALAN_OS_PUBLIC_URL` | ❌ Not set | Blocked on Cloudflare Tunnel |
| GSD | ⚠️ Partial | Skills installed, SDK path may need symlink |
| `ANTHROPIC_API_KEY` | ⚠️ Check | Prior key suffix `pzDMW` was revoked — confirm current key works |

---

## PRIORITY QUEUE — NEXT SESSION

```
1. Patch PLACEHOLDER_GMAIL → jFnLpO3jTd8SKeBR in workflow_4_1_lead_enrichment.json. Commit.
2. Set up Cloudflare Tunnel (api.veritasaipartners.com → localhost:8000). Add to Task Scheduler.
3. Set ALAN_OS_PUBLIC_URL=https://api.veritasaipartners.com in .lux/.env
4. Import + activate Workflow 4.1 via n8n UI. Test lead_id=1 (Stemilt). Confirm in SalesOS.
5. Fix GSD SDK symlink if /gsd-help errors.
6. VIE Step 2 — nlm_feed_builder.py augmentation.
```

---

## SESSION OPEN PROTOCOL

```
cd C:\Veritas\repos\alan-os
claude --dangerously-skip-permissions
```

Paste as opener:
```
Read CLAUDE.md, PROJECTS.md, and memory-bank/session-log.md. Report state.

Then execute priority queue from HANDOFF_SESSION_MAY01_2026.md 
at C:\Veritas\repos\alan-os\memory-bank\HANDOFF_SESSION_MAY01_2026.md

Priority 1: Patch PLACEHOLDER_GMAIL → jFnLpO3jTd8SKeBR in 
workflow_4_1_lead_enrichment.json. Commit.

Priority 2: Set up Cloudflare Tunnel:
  winget install cloudflare.cloudflared
  cloudflared tunnel login
  cloudflared tunnel create veritas-hub
  cloudflared tunnel route dns veritas-hub api.veritasaipartners.com
Add to Task Scheduler. Set ALAN_OS_PUBLIC_URL in .lux/.env.

Priority 3: Import + activate Workflow 4.1 via n8n UI at 
https://n8n.lorettasercy.com. Test with lead_id=1. 
Confirm lead appears in SalesOS tab.

Priority 4: Test /gsd-help. Fix SDK symlink if it errors.

Report state after reads then proceed in order.
```
