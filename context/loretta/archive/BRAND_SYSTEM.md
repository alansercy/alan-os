# MoveWithClarity — Brand System & Claude Session Primer
**Loretta Sercy · eXp Realty · lorettasercy.com**
**Version:** May 2026 | Canonical: `C:\Veritas\repos\loretta-os\BRAND_SYSTEM.md`

---

## HOW TO USE THIS DOCUMENT

Paste the contents of this file at the start of any Claude session where you are building or editing a guide page. It replaces any need to re-explain the brand, tone, compliance rules, or design system from scratch.

**Start your Claude session like this:**
> "I'm building a new MoveWithClarity guide page. Here is my brand system: [paste this file]. I'm using the guide template `loretta_guide_template.html` as my base. The guide I'm building is [guide name]. Here is the brief: [paste your brief]."

---

## WHO YOU ARE

**Loretta Sercy** — North Texas real estate advisor and Realtor® with eXp Realty.
**Brand:** MoveWithClarity
**Core positioning:** *Move with Clarity. Not Pressure.*
**Niche:** Buyers and sellers navigating meaningful life transitions — acreage, downsizing, divorce, aging parents, suburban-to-rural moves, expired listings.
**Market:** Outer DFW — Rockwall County, Caddo Mills, Greenville, Farmersville, Josephine, Blue Ridge, Royse City. Buyers moving east from Allen, Plano, McKinney.

---

## BRAND VOICE — THE RULES

### What the brand always sounds like:
- **Direct and honest** — not diplomatic. Say the real thing.
- **Warm but never sycophantic** — care is real, not performed.
- **Calm** — never urgent, never pressuring.
- **Strategic** — this is advisory, not sales.
- **Emotionally intelligent** — acknowledge what people are actually feeling.
- **Editorial/advisory** — this is a guide series, not a lead-gen funnel.

### What the brand never sounds like:
- Sales-heavy or pushy
- "Top producer" or luxury performance branding
- Trendy realtor language ("dream home," "crushing it," "game changer")
- Fear tactics or urgency manufacturing
- Generic real estate copy that could apply to any agent anywhere
- Emojis in professional or guide content

### The brand philosophy in one sentence:
> Loretta's job is not to sell anyone on a house. Her job is to help people think clearly.

---

## WRITING STYLE FOR GUIDE CONTENT

### Tone is everything.
Each guide serves a reader in emotional distress — frustrated, overwhelmed, grieving, uncertain. The writing must make them feel *seen and safe before it makes them feel informed.*

### The emotional state pattern:
Before writing any section, ask: what is this person actually feeling right now? Write to that feeling first. Then give them the information.

### Sentence rhythm:
- Short, grounded declarative sentences carry weight.
- Long sentences are for complexity, not for stuffing in information.
- Leave white space. Don't over-explain.

### Paragraph length:
- 3–5 sentences for narrative body paragraphs.
- Pull quotes, signal lists, and aside cards break up long runs of text.
- Never write walls of text in a section.

### The "diagnostic not promotional" rule:
Guide content should feel like a knowledgeable friend explaining what actually happened — not a realtor pitching for a listing. No competitive positioning against other agents. No fear of missing out. Just honest clarity.

### Strong language patterns to use:
- "The signs are rarely dramatic. They are usually quiet, incremental."
- "A home not selling doesn't automatically mean it's a bad property."
- "The resistance is usually not about the house."
- First-person Loretta voice for closing CTAs only — not in guide body.

### Language to avoid:
- "Don't miss out" / "Limited time"
- "We" (Loretta is a solo practitioner — use "I" in CTAs)
- "As your agent" (too transactional for guide content)
- Anything that implies the reader must act now

---

## WEBSITE ECOSYSTEM STRUCTURE

### Core site pages:
- Homepage
- About
- IDX / Search
- Services
- Contact
- Clarity Blueprint (signature seller process page)

### Guide series (each a standalone indexed page):
| Slug | Guide Name | Status |
|---|---|---|
| `/clarity-blueprint` | The Clarity Blueprint | ✅ Live |
| `/parents-move-guide` | The Parents' Move Guide | ✅ Live |
| `/why-your-house-didnt-sell` | Why Your House Didn't Sell | 🔨 In build |
| `/divorce-housing-clarity-guide` | The Divorce & Housing Clarity Guide | 🔨 In build |
| `/new-build-survival-guide` | New Build Survival Guide | Queued |
| `/first-time-seller-guide` | First-Time Seller Guide | Queued |
| `/before-you-leave-the-suburbs` | Before You Leave the Suburbs | Queued |
| `/multigenerational-living-guide` | Multigenerational Living Guide | Queued |
| `/acreage-transition-guide` | Acreage Transition Guide | Queued |
| `/parents-move-guide` | The Parents' Move Guide | ✅ Live |

### Wave Report series:
- `/wave-report` — hub/archive page (intro, purpose, index, latest edition, subscribe CTA)
- `/wave/[month-year]` — individual monthly report pages (e.g., `/wave/may-2026`)

### SEO philosophy:
The goal is **topical authority + trust + long-form positioning** — not generic real estate SEO. Each guide page must:
- Have its own SEO title, meta description, and OG tags
- Include internal links to related guides
- Link back to homepage and Clarity Blueprint
- Feel editorial, not lead-gen heavy

---

## DESIGN SYSTEM

### Design tokens (CSS variables — never change these):
```
--navy:        #1A2B3C
--navy-deep:   #111E2A
--navy-mid:    #243448
--gold:        #B8903C
--gold-light:  #D4AF6A
--cream:       #F5F1EB
--cream-warm:  #EDE8E0
--chalk:       #F9F7F4     ← default page background
--bluegray:    #8FA0B0
--stone:       #4A5A6A
--ink:         #1A2B3C
```

### Typography:
- **Headings / display:** Playfair Display (serif) — Google Fonts
- **Body / UI:** Jost (sans-serif) — Google Fonts
- Never use Inter, Roboto, Arial, or system fonts

### Guide accent colors (one per guide — optional but gives each guide its own feel):
- Parents' Move Guide: `#9E6B52` (terracotta — warm, familial)
- Divorce Guide: `#6B7A8F` (slate blue — calm, grounded)
- Expired Listing / Clarity Blueprint: `#8B7355` (warm taupe — diagnostic)
- Acreage/Transition guides: stay with `--gold`

### Section background rhythm:
Alternate sections: `chalk → cream → chalk → cream`
Dark sections (`--navy` or `--navy-deep`) for framework/bonus sections only.

### The template file:
`loretta_guide_template.html` — use this as your base for every new guide.
All `<!-- REPLACE: ... -->` comments tell you exactly what to fill in.
Do not change nav, footer compliance, JS, or design tokens.

---

## TREC COMPLIANCE — NON-NEGOTIABLE

**Texas is a NON-DISCLOSURE STATE.**

Rules that apply to every piece of content:
1. **Never post or share closed sale prices.** List price and days on market only.
2. **Never share price per acre at closing.**
3. **Never share specific closed transaction dollar amounts.**
4. **Always use "comps" — never "value."** Loretta is not an appraiser.
5. **License number must appear on all real estate content.**
6. **Loretta's license:** TX #0633703 · eXp Realty · Broker: Karen Richards #0508111

When in doubt: describe *process*, not *price*.

---

## CONTACT & COMPLIANCE BLOCK

Always use these exact details in footer and CTA sections:

```
Loretta Sercy
Realtor® · eXp Realty
TX License #0633703
Phone: +1 (720) 334-6799
Email: loretta.sercy@exprealty.com
Website: lorettasercy.com
Broker: Karen Richards · License #0508111
5605 N MacArthur Blvd, Irving, TX 75038
Equal Housing Opportunity
```

---

## ACTIVE GUIDE BRIEFS

### Why Your House Didn't Sell
**Target:** Homeowners with expired, withdrawn, cancelled, or stagnant listings.
**Emotional state:** Frustrated, embarrassed, disappointed, confused, defensive.
**Tone:** Calm, honest, diagnostic, non-judgmental.
**Section flow:**
01 The emotional reality of a listing that didn't sell
02 Why "more marketing" is usually not the answer
03 Pricing is not emotional — buyers compare everything
04 Buyers decide emotionally before they justify logically
05 Photos and showing experience matter more than sellers realize
06 Sometimes the market shifted while you were listed
07 The wrong buyer may have been targeted
08 Listing history changes buyer psychology
09 What to evaluate before relisting
**Bonus:** The Relisting Clarity Framework
**Style:** No attacking prior agents. No fear tactics. Feels like someone finally explaining what happened clearly.

---

### The Divorce & Housing Clarity Guide
**Target:** Individuals/couples navigating separation or divorce involving shared housing.
**Emotional state:** Overwhelmed, exhausted, uncertain, fearful, grieving.
**Tone:** Calm, safe, grounded, non-judgmental, emotionally intelligent.
**Section flow:**
01 Why housing decisions during divorce feel so overwhelming
02 The emotional mistakes people make when deciding what to do with the house
03 Keeping the house vs. selling it — what people don't fully consider
04 Understanding affordability after separation
05 Timing matters more than people realize
06 Why emotional attachment and financial reality often conflict
07 Children, stability, schools, and routine considerations
08 The importance of building the right support team
09 What to think through before making a final housing decision
**Bonus:** The Divorce Decision Clarity Framework
**Style:** No "win the divorce" energy. No legal-heavy language. No aggressive sales positioning. Prioritize dignity, stability, and long-term clarity.

---

## WHAT LORETTA'S WEBSITE SHOULD FEEL LIKE

**Should feel:**
- Intelligent
- Calm
- Strategic
- Emotionally aware
- Highly intentional
- Trust-centered
- Editorial / advisory

**Should NOT feel:**
- Sales-heavy
- Lead-gen heavy
- Trendy realtor branding
- Luxury performance branding
- Generic "top producer" marketing

---

*End of Brand System document.*
*Canonical location: `C:\Veritas\repos\loretta-os\BRAND_SYSTEM.md`*
*Last updated: May 2026*
