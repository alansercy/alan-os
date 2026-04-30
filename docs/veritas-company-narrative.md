# Veritas AI Partners — Company Narrative

**Last updated:** 2026-04-29
**Owner:** Alan Sercy
**Canonical location:** `C:\Veritas\assets\veritas\veritas-company-narrative.md`
**Required context:** loaded every session (per `CLAUDE.md` §6) for company vision, product portfolio, and exit thesis.

This file is the durable narrative spine of Veritas AI Partners. It's loaded at the start of every working session so the model has the company's identity, product strategy, financial reality, and exit thesis without re-derivation. Update only when something material changes (new product line, repositioning, new revenue stream, exit decision).

---

## 1. Identity

| Item | Decision |
|------|---------|
| Brand name | **Veritas AI Partners** |
| Tagline | **Simplifying Matters** |
| Legal entity | **CentPenny LLC** (Texas, since 2016) |
| DBA | Veritas AI Partners — Assumed Name Certificate, Rockwall County TX (~$20, **not yet filed**) |
| Brand voice | Precise. Human. Inevitable. |
| Primary color | Deep Navy `#0A1628` |
| Accent color | Electric Cobalt `#1E6FD9` (legacy) / Veritas Gold `#C6A96A` (current waitlist + dashboard kit) |
| Headline font | Cormorant Garamond |
| Body font | DM Sans |
| Brand-kit assets | `C:\Veritas\assets\veritas\veritas_brand_kit.html` · `veritas_logo_system.html` · `veritas_homepage.html` |

CentPenny LLC is the **invisible holding entity** — never customer-facing. All 1099 fractional income, AgentOS revenue, and future product LLCs flow through CentPenny.

---

## 2. Corporate Structure

```
CentPenny LLC (Parent / Holding Entity, est. 2016)
        │
        ├─── Veritas AI Partners (DBA — fractional executive consulting practice)
        │
        └─── Future product LLCs (spin out at scale)
                ├─ AgentOS LLC          (real estate AI OS)
                ├─ TradeOS LLC          (trades / logistics AI OS)
                ├─ PersonalOS LLC       (personal/executive AI OS)
                ├─ SalesAgentOS LLC     (BD / outbound AI OS)
                └─ FinanceOS LLC        (commercial moat — backburner)
```

**Spin rule:** a product line spins into its own LLC when it crosses 10 paying clients OR a meaningful funding event. Until then, every product line bills through CentPenny.

---

## 3. Two Tracks — Never Mix

| Track | Brand | Purpose |
|-------|-------|---------|
| **Personal career** | Alan Sercy | W2 or direct 1099 executive — CRO, COO, CCO, AI Transformation lead |
| **Fractional + product** | Veritas AI Partners / AgentOS / TradeOS / etc. | CentPenny LLC business — fractional engagements + product subscriptions + buildouts |

LinkedIn posts, resumes, and recruiter conversations stay on the **Alan Sercy track**. Veritas marketing, AgentOS sales, waitlist pages, and product positioning stay on the **Veritas track**. The two tracks share infrastructure (the OS stack itself) but never share brand surface or messaging.

---

## 4. Product Portfolio

The Veritas stack is a family of vertical AI operating systems. Each one solves the same shape of problem — turning fragmented manual operations into a continuously-running AI infrastructure — for a specific buyer. AgentOS is the live proof; the others extend the pattern.

### AgentOS — Real Estate Agent + Brokerage OS
**Status:** Live proof of concept (Loretta Sercy / eXp Realty) + first commercial pilot (MMM Trucking-adjacent agent base, planned).

AI operating system for real estate agents and brokerages. Inbox triage, content engine, lead routing, follow-up sequences, listing brief generation. Built and proven on Loretta's live business.

**Live proof:**
- Inbox: 27,500 → 3,400 emails (88% reduction)
- Content engine: built and running (Workflows 2.1, 2.2, 2.4, 2.5, 2.6, C — Telegram intake)
- Side-hustle revenue: $5K/mo (Loretta operations)
- Workflow 2.4 (video repurposing) deployed + active 2026-04-29 — webhook live at `https://n8n.lorettasercy.com/webhook/video-repurpose`

**Pricing tiers:**
| Tier | Price | What's included |
|------|-------|----------------|
| Bronze | $497–$997/mo | DIY kit, onboarding docs, templates, self-setup |
| Gold | $1,000–$2,500 setup + monthly | Done-with-you, 30-day onboarding, custom config |
| Platinum | $2,500–$5,000 buildout + retainer | Done-for-you, full buildout, ongoing management |
| eXp Discount | 50% off Bronze | Recruiting tool — agents joining under Loretta at eXp |

**Buyers:** solo agents, small brokerages, eXp downline.

**White space (Apr 2026 competitive scan):** Lofty AOS ($299+/mo, brokerage-first, too expensive for solo) and Breezy ($10M pre-seed, waitlist, luxury focus) own the upper end. Nobody owns the **solo agent + eXp ecosystem** intersection at the $497–$997 price point. Window closes when Breezy goes live.

### TradeOS — Trades / Logistics SMB OS
**Status:** Pilot via MMM Trucking ($3K/mo retainer, active).

AI business development for trucking, HVAC, plumbing, and trades. Pipeline runs while the operator works the field. Inbox triage, prospect audit, hot-lead SMS alerts, SOP generation on close.

**Live infrastructure:**
- Workflow 3.1 — MMM Gmail triage (active)
- Workflow 3.2 — MMM prospect audit (ready to fire)
- Workflow 2.3 — Hot Lead SMS (skeleton built, blocked on Twilio account setup)

**Buyers:** owner-operator and family-run trade SMBs $1M–$25M revenue, financial services, debt collection.

### PersonalOS — Executive + Family-Steward OS
**Status:** Live for Alan (Lux Stack, dashboard, Norman Inbox Guard); first commercial buildout TBD.

Personal AI operating system for executives and family stewards. Email triage across multiple accounts, family inbox guardianship, knowledge hub, vault, dashboard. The premise: your personal life runs like a business — automate accordingly.

**Live infrastructure (Alan):**
- Alan OS Dashboard at `localhost:8000/dashboard` (Phases 1–4 done; Phases 5–6 queued)
- Norman Inbox Guard (daily 6 AM digest, 14-address whitelist, USAA auto-routing, Marsha forwarding staged)
- Email triage across 5 accounts (MSN, Gmail, Loretta, Keys, MMM)
- Drive integration across 6 canonical assets

### SalesAgentOS — BD / Outbound AI OS
**Status:** V1 dashboard tab live (Lux Command Center, 2026-04-29); Workflow 4.1 (lead enrichment) spec'd, pending build.

Outbound business-development infrastructure for fractional executives, B2B founders, and SMB owners. Lead intake, enrichment via Claude, stage tracking, competitor intel. Trigger for Workflow 4.1 = **n8n webhook direct** (`POST https://n8n.lorettasercy.com/webhook/salesos-enrich`, decision captured 2026-04-29).

**Pipelines tracked:** veritas_bd · loretta_re · mmm_trucking · personalos · agentos · tradeos · personal.

### FinanceOS — Commercial Moat (Backburner)
**Status:** Highest long-term moat. Not active. Do not start until MMM + digital presence revenue is stable AND the job search is resolved.

AI finance agent for nightly transaction reconciliation, revenue tracking, financial reporting, commission calc. First planned client = the Veritas/MMM revenue stack itself ($6K/mo MMM + $18K catch-up + Stemilt pipeline).

**Architectural needs (deferred):** bank/transaction data source, Sheets or Quickbooks integration, nightly Claude API call for categorization + anomaly detection, morning summary report.

### Veritas Intelligence Engine (VIE) — Cross-OS Research Radar
**Status:** V1 in build (Workflow 5.1 — Python-first; endpoints + per-URL enrichment landed 2026-04-29 lux-os `952862e` + `e990881`).

Autonomous AI research radar. Walks inbox + (V2) GitHub trending + RSS + X/Twitter saves. Claude enriches each URL (summarize, score relevance 0–10, fit-tag against Veritas/AgentOS/PersonalOS pipelines). Persists to `~/.lux/Data/ai_stack_feed.json`. Surfaces ranked recommendations on the dashboard.

**Why it matters:** eliminates the manual "save link, read later, evaluate" loop. Sellable component inside PersonalOS and AgentOS — every executive client has the same problem.

### Digital Presence — Veritas Service Line
**Status:** Active — painter client website in build (demo upcoming); health enthusiast queued.

Done-for-you websites + brand systems for SMB clients. Reusable Offer Sheet template extracts after first SOW. Evaluating cto.new pipeline (polished scaffold → Claude Code customization → Netlify deploy → user-owned) against direct Claude Code build for speed/quality/cost.

---

## 5. Financial Picture (as of 2026-04)

| Source | Monthly | Annual |
|--------|---------|--------|
| Loretta 3PL day job | ~$10,000 | ~$120,000 |
| Loretta side-hustle (Alan running) | ~$5,000 | ~$60,000 |
| MMM Trucking retainer (Veritas) | $3,000 | $36,000 |
| Alan unemployment | $2,000 | $24,000 |
| **Total in** | **~$20,000** | |
| Monthly nut | ~$24,000 | |
| **Monthly deficit** | **~$4,000** | |
| Savings runway | ~$60,000 | ~5 months |

**Revenue targets:**
- $600K run rate by month 6
- $1.2M run rate by month 12

**S-Corp election decision** on CentPenny LLC needs CPA conversation **before** revenue scales — pending.

---

## 6. Revenue Streams — Priority Order

| Priority | Stream | Target | Timeline |
|----------|--------|--------|---------|
| 1 | Fractional CRO/COO/CCO engagement | $8K–$25K/mo | Close in 30 days |
| 2 | AgentOS Bronze/Gold subscribers | $500–$2,500/mo each | Month 2–3 |
| 3 | Loretta real estate commissions | Replace $120K/yr | Month 3–6 |
| 4 | AgentOS Platinum buildouts | $2,500–$5,000 + retainer | Month 3+ |
| 5 | TradeOS pilots beyond MMM | $3K–$8K/mo each | Month 4–6 |
| 6 | Digital Presence websites | $3K–$15K/project | Continuous |
| 7 | PersonalOS buildouts | $5K–$15K + retainer | Month 6+ |

---

## 7. Fractional Executive Positioning (Alan Sercy track)

**Elevator:** "I'm a fractional executive with 30 years building and scaling revenue operations in financial services, mortgage, and tech-enabled businesses. I work with PE-backed companies, early-stage investors, and entrepreneurial operators who need a seasoned CRO, COO, or AI transformation leader without the full-time cost. And I bring something most fractional execs can't — a fully built AI operating system that deploys on day one and makes your team 3× more productive immediately."

**NotebookLM-generated executive summary:**
"High-impact Fractional CRO/COO specializing in AI-driven operational excellence for PE-backed firms and growth-stage financial services. I deploy a turnkey AI operating stack on day one to drive immediate EBITDA expansion, accelerating your 'speed to value' by automating complex regulatory and operational workflows. My track record includes securing $9 Billion in whole-loan mortgage products during market downturns and transforming a $4M annual loss into a profitable entity. I bring a proven ability to scale high-margin divisions, evidenced by building a $27M revenue partnership unit that achieved 12% growth during global volatility. By bridging the gap between legacy systems and modern intelligence, I de-risk the AI transition for entrepreneurial CEOs while 'Simplifying Matters' through automated operational rigor."

**Proof points:**
- $9B whole-loan mortgage product architected
- $27M strategic partnership unit built from zero (12% growth during pandemic)
- $4M annual loss → profitable turnaround (ClearSpring)
- $21M student-loan-servicing unit (TSI Interim President)
- 30 years across mortgage, debt collection, SaaS, PE-backed firms

**Target verticals:** mortgage, financial services, debt collection, SaaS, PE-backed growth companies, AI-native startups.

**Engagement model:** flexible — monthly retainer, project-based, or equity + retainer.

**PE-language hooks:**
- AI-Driven EBITDA Expansion
- De-risking the AI Transition
- Speed to Value — day-one deployment
- Automated Operational Rigor

**Tier-1 warm outreach (active):**
1. **Rocktop Technologies** — current employer; fractional transition
2. **Transworld Systems (TSI)** — former Interim President; AI transformation advisor
3. **Mercury** — cold; AI-powered revenue operations, $27M partnership proof point

---

## 8. Go-to-Market — Authority + Waitlist Layer

The marketing engine sits **upstream** of the products. Two pieces:

### LinkedIn Authority Track (Alan Sercy)
B2B personal-brand engine targeting PE-backed operators, startup founders, SMB owners. **Separate from Loretta's real-estate content.** Voice: 28-year revenue executive who builds and deploys AI ops systems — not a tech vendor, a trusted advisor.

**Pillars (3):**
1. Revenue-operations war stories — 28 years of closes, turnarounds, lessons
2. AI in the field — what actually works (MMM, AgentOS, real results, no hype)
3. Executive perspective on AI — where the market is going, what operators get wrong, what to build vs. buy

**Cadence:** 3× per week minimum once launched. Short-form text first; video repurposing second.

### Waitlist Pages (Veritas)
One landing page per OS vertical. **Each page goes live BEFORE the full product is built.** <10 signups in 30 days → do not build that vertical. ≥10 → green light. AgentOS is the exception (already deployed for MMM — used as social proof).

**Subdomains:**
- `agentos.veritasaipartners.com`
- `tradeos.veritasaipartners.com`
- `personalos.veritasaipartners.com`

**Stack:** single HTML file per page · Veritas brand kit (Navy `#0B1E3D`, Gold `#C6A96A`, DM Sans + Cormorant Garamond) · Netlify Forms email capture · 3-email Claude-drafted nurture sequence (confirmation → week-2 result → launch).

**Strategic role:** the MMP validation gate. No more building OS verticals without a waitlist signal first.

---

## 9. Exit Thesis

The endgame is a **CentPenny LLC holding-company sale** (or partial-stake transaction) once:

1. Two product LLCs (most likely AgentOS + TradeOS or AgentOS + PersonalOS) hit independent revenue thresholds — 100+ paying clients each, $50K+/mo each
2. Recurring revenue across the stack ≥ $200K/mo for 12+ consecutive months
3. The shared OS infrastructure (orchestration engine ORCH-1/2/3, dashboard, n8n workflow library, NotebookLM intelligence loop) is documented + transferable

**Buyer thesis:**
- Vertical SaaS roll-ups looking for AI-native bolt-ons
- PE-backed real estate, trades, or business-services platform plays
- AI infrastructure companies wanting commercial proof of vertical AI OS deployments

**Defensibility:**
- **Live commercial proof** in real estate (Loretta) and trucking (MMM) before any pitch
- **Shared orchestration engine** (ORCH-1/2/3) that runs across verticals — buyer gets the engine, not just one product
- **Veritas Intelligence Engine** as the cross-OS research radar — one piece of infrastructure that powers every vertical's content + competitive intel layer
- **FinanceOS as the moat** — when activated, the data + automation create switching costs the competition can't match

**Track separation enables exit optionality:** Alan Sercy's W2 / fractional career stays liquid (resumes, LinkedIn, recruiter relationships) regardless of CentPenny outcome. CentPenny can sell, partial-sell, or continue independently without affecting the personal track.

---

## 10. Standing Rules (do not revisit)

These are **locked decisions** — do not re-debate without an explicit reopen.

- Brand name: Veritas AI Partners
- Tagline: Simplifying Matters
- Legal: CentPenny LLC DBA Veritas AI Partners
- Holding-company structure: CentPenny is the parent; products spin into LLCs at scale
- Two tracks separate: Alan Sercy (career) vs Veritas AI Partners (business)
- AgentOS pricing tiers (Bronze/Gold/Platinum/eXp Discount)
- eXp recruiting discount: 50% off Bronze
- Content scheduler: n8n + Buffer node (free — replaces Zernio)
- Brand Constitution: 7 rules (in `veritas_brand_kit.html`)
- Email pipeline: Outlook COM → Claude Haiku → Veritas Feed Doc → NotebookLM
- Veritas Feed canonical Doc ID: `1WD2Sr2HgSdMffSYv9bWIpPZOoef4_LDH27yQBiuuM6M`
- Required-context narrative: this file, loaded every session

---

## 11. References

- **Source handoff:** `C:\Veritas\assets\veritas\Veritas_Handoff.md` (2026-04-11 — origin document for §1, §2, §3, §5, §7)
- **Status board:** `C:\Veritas\repos\alan-os\PROJECTS.md` (live — origin for §4, §6, §8)
- **Brand kit:** `C:\Veritas\assets\veritas\veritas_brand_kit.html` · `veritas_logo_system.html` · `veritas_homepage.html` · `veritas_pitch_deck.html`
- **Offer sheets / signal docs:** `agentos_offer.html` · `tradeos_offer.html` · `personal_os_intake.html` · `veritas_signal_gigi.html` · `veritas_signal_roel.html`
- **AI stack diagram:** `C:\Veritas\assets\veritas\veritas_ai_stack.svg`
- **Strategy notes:** `C:\Veritas\strategy\veritas_strategy.md`
- **Session protocol:** `C:\Veritas\repos\alan-os\SESSION_PROTOCOL.md`

---

*Maintained by Alan Sercy. Update on material changes only — new product line, repositioning, new revenue stream, exit decision, locked-rule reversal.*
