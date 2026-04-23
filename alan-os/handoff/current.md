# Alan OS · Current Handoff
**Last Updated:** April 22, 2026
**Session Type:** Lollie & Lovie Lou Website Build + Deploy + GitHub Memory Architecture Setup
**Environment:** Host · alansercy@gmail.com

---

## How to Load This Context

Paste at the start of any Claude session:
```
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/handoff/current.md
```

For strategy sessions add the relevant domain file:
```
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/veritas_strategy.md
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/lollie_brand.md
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/mmm_trucking.md
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/job_search.md
Load: https://raw.githubusercontent.com/alansercy/alan-os/main/strategy/family_governance.md
```

---

## Immediate Actions — Do These First

1. **Check lollieandlovielou.com on mobile** — mobile optimization built but not reviewed. Flag layout issues next session.
2. **Google Workspace email** — loretta@lollieandlovielou.com + hello@ alias. $7/mo Workspace Starter. TXT verification goes in Netlify DNS panel (not GoDaddy — nameservers already switched).
3. **Norman Inbox Guard digest** — arrives daily 6AM at alansercy@gmail.com. Review filtered senders, add legit ones to `norman_whitelist.txt`.
4. **Claude token dashboard** — bat file fix needed: malformed `set ANTHROPIC_ADMIN_API_KEY=` line. Add Norman AOL inbox + manual run button. ⬜
5. **Dashboard dismiss behavior** — clarify job search pending page: does dismiss delete? ⬜
6. **Remaining strategy files** — mmm_trucking.md, job_search.md, family_governance.md not yet built. ⬜
7. **Veritas positioning paragraph** — still the blocker for Rocktop/TSI/Mercury outreach. Multiple sessions open.
8. **HP Hood — Matthew Bauer** — May 1 deadline LIVE. Outbound kit ready.
9. **Stemilt — Gordy Schulze** — warm intro via Brendan. Next after Hood.

---

## Session Completed Items

### ✅ Memory Architecture — GitHub Live
- **Repo:** github.com/alansercy/alan-os (private)
- **Session load protocol:** Paste raw GitHub URL at session start — no re-explaining ever again
- **Files live:** README.md, handoff/current.md, strategy/veritas_strategy.md, strategy/lollie_brand.md, sops/lux_stack.md
- **Still needed:** mmm_trucking.md, job_search.md, family_governance.md, sops/norman_inbox_guard.md, vault/ structure

### ✅ Lollie & Lovie Lou Website — LIVE
- **URL:** lollieandlovielou.com
- **Netlify site:** lolliewebsitefinal
- **Deploy:** Drag index.html + resource-guide.html to Deploys tab — instant, no propagation ever again
- **DNS:** GoDaddy nameservers → Netlify (dns1-4.p03.nsone.net) — permanent
- **Photos:** All baked into index.html as base64 — no images folder needed
- **Resource guide gate:** Netlify Forms capturing signups — check app.netlify.com → lolliewebsitefinal → Forms
- **Shop tab:** Greyed out "Coming Soon" — activate after Printful samples approved

### ✅ Norman Inbox Guard — Live
- **Script:** `C:\Users\aserc\.lux\norman_inbox_guard.py`
- **Schedule:** Daily 6AM via Task Scheduler
- **Digest:** Sent to alansercy@gmail.com
- **Whitelist:** `C:\Users\aserc\.lux\norman_whitelist.txt` — 14 addresses + 2 domain rules
- **Forwarding to Marsha:** Staged, disabled — flip `FORWARDING_ENABLED = True` when ready

---

## 01 · Website File Registry

| File | Contents | Status |
|------|----------|--------|
| `index.html` | Full homepage — 1.5MB with embedded photos | Live |
| `resource-guide.html` | Family Resource Guide — updated copy + disclaimers | Live |

**Photo mapping:**

| Original | Embedded As | Placement |
|---|---|---|
| heropage_lollieandlovielou.jpg | hero.jpg | Hero — nose-to-nose kiss, full half-screen |
| lunch.jpg | restaurant.jpg | Our Story — EXIF rotation fixed |
| B2.jpeg | houndstooth.jpg | Strawberry moment — cropped head-to-boots |
| carshow1.jpeg | carshow1.jpg | The Car Show — photo 1 |
| carshow2.jpeg | carshow2.jpg | The Car Show — photo 2 |
| carshow3.jpeg | carshow3.jpg | The Car Show — photo 3 |
| Cruise.jpg | cruise.jpg | About Loretta + Don't Shrink Their World |
| B_plane.jpeg | plane.jpg | Don't Shrink Their World |
| Happy_Halloween.jpeg | halloween.jpg | Don't Shrink Their World |
| happy_apple.jpg | *(not used)* | — |
| mad_apple.jpg | *(not used)* | — |

---

## 02 · Homepage Structure (Emotional Order)

1. Hero — kissing shot + title + 3-line subheading + actions
2. Emotional Hook Band — "This series does not focus on what she cannot do..."
3. Our Story — restaurant photo + perspective shift callout
4. Real Moments — The Car Show (3-photo grid) + The Strawberry
5. Don't Shrink Their World — 4-photo grid + copy
6. The Series — 4 book cards
7. Resource Guide Band — green, gated CTA
8. About Loretta — cruise photo + bio
9. Email Capture — early reader list
10. Footer — nav + disclaimer + copyright

**Nav:** Our Story · Real Moments · The Series · Resource Guide · About Loretta · Shop (Coming Soon) · Join the List
**Butterfly:** 320px, top-right of hero, floating SVG — no external dependency

---

## 03 · Resource Guide Gate

- Click any "Free Resource Guide" → modal → First Name + Email → submit
- Netlify Forms captures silently in background
- Success state → "Open the Resource Guide →" → resource-guide.html
- Check signups: app.netlify.com → lolliewebsitefinal → Forms tab
- Export: Download CSV anytime
- Connect Mailchimp later: native Netlify integration, 20 min setup

---

## 04 · Resource Guide Copy Changes Applied

| Change | Old | New |
|--------|-----|-----|
| Disclaimer | (none) | "About This Guide" — lived experience, not medical advice |
| Nutrition | "gut-brain...affects everything" | "We noticed nutrition had a significant impact on Brielle's..." |
| Magnesium bath | "It has never failed us" | "For Brielle, it consistently helped calm her nervous system" |
| Outdoor time title | "not optional" | "For Brielle, outdoor time became essential" |
| Outdoor time body | Universal claim | Grounded in Brielle's daily rhythm |
| Early intervention | "is everything" | "made a profound difference" |
| Footer | Copyright only | Disclaimer + copyright |

Supplement disclaimer kept exactly: "Always work with a doctor — never supplement without testing first."

---

## 05 · Printful Shop SOP — Delivered

**File:** printful_sop.pdf — 3-page internal SOP

| Shirt | Base | Price | Key Line |
|-------|------|-------|----------|
| Supporter Tee | Bella Canvas 3001 Adult | $28–32 | "Ability is everywhere. You just have to look." |
| Lollie Tee | Bella Canvas 3001 Adult | $28–32 | "I don't see a mess. I see a mind at work." |
| Car Show Director | Bella Canvas 3001 Youth | $22–25 | Red Porsche silhouette + "Car Show Director" |

Store connection: Static HTML site → recommend Etsy (free) or Shopify Starter ($5/mo) as storefront linked from Shop tab.

---

## 06 · DNS & Netlify State

| Item | Status |
|------|--------|
| GoDaddy nameservers | Switched to Netlify dns1-4.p03.nsone.net |
| lollieandlovielou.com | Connected to lolliewebsitefinal |
| www.lollieandlovielou.com | Auto-redirects to primary |
| SSL cert | Auto-provisioned |
| Google Workspace TXT | NOT YET ADDED — needed for email setup |
| Netlify Forms | Active — capturing signups |

---

## 07 · Open Workstream State

### Veritas AI Partners ⚠️
- Blocker: Positioning paragraph not written — blocking Rocktop, TSI, Mercury
- Entity: CentPenny LLC (DBA Veritas AI Partners)
- Offers: FinanceOS (offer doc needed), SalesAgentOS (offer doc needed), AgentOS (Bronze/Gold/Platinum locked)
- Open context: Rudy Casanova, Chris Connelly
- Full strategy: github.com/alansercy/alan-os/strategy/veritas_strategy.md

### MMM Trucking — Active
- Lane: NorCal → WA → UT/ID → return CA · Refrigerated food-grade · Direct shippers only
- Prospect Tracker: Google Sheets 1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI (lsercy@mmmtrucks.com)
- HP Hood: Matthew Bauer — May 1 deadline LIVE
- Stemilt: Gordy Schulze — warm intro via Brendan
- Nimrat call: Commission trigger, rate, payment terms in writing — this week

### Job Search — Active
- Target: Remote CRO or EVP BD · $150K floor · $200K+ target with equity
- Brief: Google Drive 1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ

### Estate Planning — Active
- Charles property: Title vesting, loan obligations, probate exposure, communication strategy
- USAA insurance claim: Norman/Marsha — Pete (sercypete@aol.com) in thread
- Estate Planning CC doc: ID pending

### Lux Stack — Live ✅
- Five accounts running via lux_launcher.py
- open issue: review_new_senders.py COM error — fix: Outlook kill/restart + sync wait
- Claude Usage Dashboard: localhost:8081 — bat file key fix still needed

---

## 08 · Drive Asset Registry

| Asset | Account | ID |
|-------|---------|-----|
| Handoff Doc (master Google Doc) | alansercy@gmail.com | 1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ |
| Lux Command Center | alansercy@gmail.com | 1hFOBfaKxBs1ZsP9hBfOXb17JZylScxkVRPpA6c0YWDc |
| Job Search Brief | alansercy@gmail.com | 1PyDF_KKLmfE9uk5cDsHogKUzb55RNQWbwbJfxg7jwAQ |
| Veritas AI Research Feed | alansercy@gmail.com | 1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M |
| MMM Prospect Tracker | lsercy@mmmtrucks.com | 1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI |
| Loretta Content Calendar | lorettasercy@gmail.com | 1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM |
| NLM Inbox Feed folder | alansercy@gmail.com | 1PIP2g8wVrtDON8FQ56PIsTTmxrrtJEMN |
| Duplicate NLM doc (retire) | alansercy@gmail.com | 1f3RGBRlmFr7b4Mb-94RoAydAn3ClnmjFN2eO7VLeVyg |
| Estate Planning CC | alansercy@gmail.com | ID pending |

---

## 09 · GitHub Repo State — alansercy/alan-os

| File | Status |
|------|--------|
| README.md | ✅ Live |
| handoff/current.md | ✅ Live — this file |
| strategy/veritas_strategy.md | ✅ Live |
| strategy/lollie_brand.md | ✅ Live |
| sops/lux_stack.md | ✅ Live |
| strategy/mmm_trucking.md | ⬜ Not built yet |
| strategy/job_search.md | ⬜ Not built yet |
| strategy/family_governance.md | ⬜ Not built yet |
| sops/norman_inbox_guard.md | ⬜ Not built yet |
| vault/ | ⬜ Not built yet |

---

*Alan OS · Veritas AI Partners · Lollie & Lovie Lou*
