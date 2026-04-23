# Alan OS · Current Handoff
**Last Updated:** April 22, 2026
**Session Type:** Lollie & Lovie Lou Website Build + Deploy + GitHub Setup
**Environment:** Host · alansercy@gmail.com

---

## Resume Instructions

Paste this at the start of any Claude session to restore full context:
```
Load context: https://raw.githubusercontent.com/alansercy/alan-os/main/handoff/current.md
Load strategy for relevant domain as needed.
```

---

## Immediate Actions — Do These First

1. **Mobile review** — check lollieandlovielou.com on phone, flag layout issues
2. **Google Workspace email** — loretta@lollieandlovielou.com + hello@ alias ($7/mo). TXT verification goes in Netlify DNS panel.
3. **Norman Inbox Guard digest** — arrives daily at 6AM at alansercy@gmail.com. Review filtered senders, add legit ones to `norman_whitelist.txt`
4. **Claude token dashboard** — bat file fix needed: malformed `set ANTHROPIC_ADMIN_API_KEY=` line. Add Norman AOL inbox + manual run button.
5. **Veritas positioning paragraph** — still the blocker for Rocktop/TSI/Mercury outreach. Multiple sessions open.
6. **HP Hood — Matthew Bauer** — May 1 deadline LIVE. Outbound kit ready.
7. **Stemilt — Gordy Schulze** — warm intro via Brendan. Next after Hood.
8. **GitHub alan-os repo** — just created. Load all strategy files next session.

---

## Active Project State

### Lollie & Lovie Lou — LIVE ✅
- **URL:** lollieandlovielou.com
- **Netlify site:** lolliewebsitefinal
- **Deploy:** Drag index.html + resource-guide.html to Deploys tab — instant
- **DNS:** GoDaddy nameservers → Netlify (dns1-4.p03.nsone.net) — permanent
- **Photos:** All baked into index.html as base64 — no images folder needed
- **Resource guide gate:** Netlify Forms capturing signups — check app.netlify.com → Forms
- **Shop tab:** Greyed out "Coming Soon" — activate after Printful samples approved
- **Next:** Google Workspace email, Printful account, mobile review

### Norman Inbox Guard — LIVE ✅
- **Script:** `C:\Users\aserc\.lux\norman_inbox_guard.py`
- **Schedule:** Daily 6AM via Task Scheduler
- **Digest:** Sent to alansercy@gmail.com
- **Whitelist:** `C:\Users\aserc\.lux\norman_whitelist.txt` — 14 addresses + 2 domain rules
- **USAA routing:** Auto-routed to Inbox/USAA folder
- **Forwarding to Marsha:** Staged, disabled — flip `FORWARDING_ENABLED = True` when ready
- **Logs:** `C:\Users\aserc\.lux\logs\norman_guard_YYYY-MM-DD.log`

### Lux Stack — LIVE ✅
- **Launcher:** `C:\Users\aserc\.lux\workflows\lux_launcher.py`
- **Accounts:** asercy@msn.com, alansercy@gmail.com, lorettasercy@gmail.com, loretta.keysandcommunity@gmail.com, lsercy@mmmtrucks.com
- **Open issue:** `review_new_senders.py` COM "exhausted shared resources" — fix: Outlook kill/restart + sync wait before re-testing (Loretta Gmail background sync conflict)

### Claude Usage Dashboard — PARTIAL ⚠️
- **Running at:** localhost:8081
- **Blocker:** `start_alan_os.bat` has malformed `set ANTHROPIC_ADMIN_API_KEY=` line
- **Next:** Fix bat file, add Norman AOL inbox, add manual run button

### MMM Trucking — ACTIVE
- **Lane focus:** NorCal → WA → UT/ID → return CA
- **Cargo:** Refrigerated food-grade, direct shippers only
- **Prospect Tracker:** Google Sheets `1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI` (lsercy@mmmtrucks.com)
- **Outbound kit:** 3-touch email sequence + voicemail scripts + 11 call situations — delivered
- **HP Hood:** Matthew Bauer — May 1 deadline LIVE
- **Stemilt:** Gordy Schulze — warm intro via Brendan
- **Nimrat call:** Commission trigger, rate, payment terms in writing — this week

### Veritas AI Partners — ACTIVE ⚠️
- **Blocker:** Positioning paragraph not written — blocking Rocktop, TSI, Mercury outreach
- **Entity:** CentPenny LLC (DBA Veritas AI Partners)
- **Brand:** Deep Navy/Electric Cobalt · Cormorant Garamond/DM Sans · "Precise. Human. Inevitable."
- **Offers:** FinanceOS, SalesAgentOS, AgentOS (Bronze/Gold/Platinum)
- **Open:** Rudy Casanova context, Chris Connelly context

### Job Search — ACTIVE
- **Target:** Remote CRO or EVP BD · $150K floor · $200K+ target with equity
- **Brief:** Google Drive `1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ`

### Estate Planning — ACTIVE
- **Charles property:** Title vesting, loan obligations, probate exposure, communication strategy
- **Estate Planning CC doc:** ID pending
- **USAA insurance claim:** Norman/Marsha — Pete (sercypete@aol.com) in thread

---

## Drive Asset Registry

| Asset | Account | ID |
|---|---|---|
| Handoff Doc (master) | alansercy@gmail.com | 1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ |
| Lux Command Center | alansercy@gmail.com | 1hFOBfaKxBs1ZsP9hBfOXb17JZylScxkVRPpA6c0YWDc |
| Job Search Brief | alansercy@gmail.com | 1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ |
| Veritas AI Research Feed | alansercy@gmail.com | 1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M |
| MMM Prospect Tracker | lsercy@mmmtrucks.com | 1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI |
| Loretta Content Calendar | lorettasercy@gmail.com | 1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM |
| NLM Inbox Feed folder | alansercy@gmail.com | 1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN |
| Duplicate NLM doc (retire) | alansercy@gmail.com | 1f3RGBRlmFr7b4Mb-94RoAydAn3ClnmjFN2eO7VLeVyg |
| Estate Planning CC | alansercy@gmail.com | ID pending |
