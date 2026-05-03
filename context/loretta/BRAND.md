# Loretta Sercy — Canonical Brand Reference
**Consolidated from:** LORETTA_BRAND.md + loretta-sercy-brand-voice-guidelines.md
**Agent:** Loretta Sercy · Realtor® · eXp Realty · TX License #0633703 · lorettasercy.com · 720.334.6799
**Last updated:** May 2026 · Scheme: Slate & Fog · Fonts: DM Serif Display + DM Sans

> Every Loretta build starts here. Read top to bottom before writing a line of code or copy.

---

## IDENTITY

**Brand name:** MoveWithClarity
**Agent name:** Loretta Sercy
**Positioning:** North Texas real estate advisor. Life transition specialist.
**Energy:** Calm authority. Advisor/consultant — not agent marketing.
**Not:** Farmhouse lifestyle. Urgency-driven. Agent-centric. Generic real estate.

### Taglines
| Use | Line |
|---|---|
| Primary | "Move with Clarity. Not Pressure." |
| Short form | "Clarity before pressure." |
| Philosophy | "Clarity protects people. Pressure costs them." |

### Wordmark formats
- **Light bg:** `Loretta` (DM Sans 300) + `Sercy` (DM Serif italic, gold)
- **Dark bg:** same, cream + fog-gold
- **Monogram:** LS in gold border box + "Move with Clarity" label
- **Compliance line:** `Loretta Sercy · Realtor® · eXp Realty · TX #0633703 · lorettasercy.com`

---

## COLOR TOKENS

```css
:root {
  --slate:       #1C2B3A;  /* Dark anchor — headers, dark sections, primary on light */
  --steel:       #2A3F52;  /* Mid dark — alternate dark cards, transitions */
  --gold:        #B8963E;  /* Primary accent — eyebrows, dividers, CTAs, borders on dark */
  --fog-gold:    #D4B96A;  /* Soft accent — subheads on dark, pull quotes */
  --slate-wash:  #ECF0F4;  /* Warm bg — alternating sections, card fills */
  --cool-white:  #F7F8F9;  /* Dominant bg — most sections */
  --ink:         #3A4A5C;  /* Body text on light */
  --mist:        #EEF2F6;  /* Text on dark backgrounds */
  --border:      #D8DEE6;  /* Card and table borders on light */

  --gold-20:     rgba(184,150,62,0.20);
  --gold-40:     rgba(184,150,62,0.40);
  --mist-60:     rgba(220,230,240,0.60);
  --mist-85:     rgba(220,230,240,0.85);
}
```

### Section background pairing
| Background | Use for | Text | Accent |
|---|---|---|---|
| `--slate` | Hero, voice, cover, dark emphasis | `--mist` / `--mist-85` | `--gold` / `--fog-gold` |
| `--cool-white` | Primary content, dominant | `--ink` | `--gold` |
| `--slate-wash` | Alternating sections, process | `--ink` | `--gold` |
| `--gold` | CTA strip, footer only | `--slate` | — |

---

## TYPOGRAPHY TOKENS

```css
/* Font import */
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@200;300;400;500&display=swap" rel="stylesheet">
```

| Token | Family | Size | Weight | Notes |
|---|---|---|---|---|
| Display | DM Serif Display | 52px | 400 | Main headlines. `em` → italic + gold |
| Display italic | DM Serif Display | 52px | italic | Paired with display for emphasis word |
| D2 / Section head | DM Serif Display | 36px | 400 | Section titles |
| Subhead | DM Serif Display | 22px | italic | Gold on light, fog-gold on dark |
| Pull quote | DM Serif Display | 26px | italic | Mist text, gold left border 2px |
| Body | DM Sans | 15px | 300 | 1.9 line-height. Ink on light |
| Body small | DM Sans | 13px | 300 | Secondary copy, card body |
| Eyebrow | DM Sans | 10px | 300 | 0.34em spacing, uppercase, gold, line prefix |
| Label | DM Sans | 9px | 400 | 0.26em spacing, uppercase, ink |
| Fine / compliance | DM Sans | 9px | 200 | 0.2em spacing, uppercase, muted |

### Responsive overrides (max-width: 768px)
- Display: 34px
- Section padding: 48px 24px
- All grids: single column

---

## SPACING SYSTEM

| Token | Value | Use |
|---|---|---|
| Micro | 4px | Label → value, icon gaps |
| Tight | 8px | Badge padding |
| Close | 12px | Eyebrow → headline |
| Item | 20px | List items, card interior |
| Block | 28px | Headline → body, card padding |
| Section internal | 36px | Rule margins, subsection gaps |
| Breath | 48px | Between major content blocks |
| Section | 72px | Full section padding, desktop |
| Page margin | 64px | Horizontal padding, desktop |
| Mobile margin | 24px | Horizontal padding, <768px |
| Max width | 960px | All content caps here |
| Prose max | 640px | Body copy line length |
| Section gap | 6px | Between adjacent flush sections |

---

## COMPONENT REFERENCE

### Dividers
```css
.rule        /* gold 0.5px, opacity 0.4 — section intro */
.rule-dark   /* slate 0.5px — content break on light */
.rule-light  /* mist 0.5px, opacity 0.3 — break on dark */
.diam-rule   /* gold lines + rotated diamond center — editorial pause */
.abar        /* left border 2.5px gold + flex gap — emphasis passage */
```

### Badges (one per element max)
```css
.badge.badge-gold     /* gold bg, slate text — primary status */
.badge.badge-outline  /* slate border + text — secondary */
.badge.badge-wash     /* slate-wash bg, gold text — context */
.badge.badge-dark     /* slate bg, fog-gold text — on light sections */
```

### Buttons (max 2 per section)
```css
.btn.btn-primary     /* slate bg, mist text — main CTA */
.btn.btn-gold        /* gold bg, slate text — secondary CTA */
.btn.btn-ghost       /* transparent, gold border + text — low-pressure invite */
.btn.btn-ghost-light /* transparent, mist border + text — ghost on dark */
```

### Cards
```css
.card        /* white bg, border — primary container on wash/white sections */
.card-wash   /* slate-wash bg, border — secondary context */
.card-dark   /* white 6% bg, gold border 45% — on dark sections */
.callout     /* gold border + gold-20 bg — editorial highlight on light */
.callout-dark /* gold border 50% + gold-10 bg — editorial highlight on dark */
```

### Layout patterns
- **A — Stat row:** `.g4` of `.stat-block` / `.stat-n` / `.stat-l`
- **B — Callout:** `.callout` wrapping `.abar` with subhead + body
- **C — Timeline:** 80px/1fr grid, italic gold week label, title + body-sm
- **D — Card grid:** `.g2` of `.card` with eyebrow + subhead + body-sm
- **E — Pull quote strip:** dark bg, `.pull` left-aligned, compliance right-aligned

---

## TREC COMPLIANCE RULES

- **Compliance line required on all public-facing materials:**
  `Loretta Sercy · Realtor® · eXp Realty · TX #0633703 · lorettasercy.com`
- **Fine print style:** DM Sans 9px, weight 200, 0.2em spacing, uppercase, muted
- Texas law requires brokerage name and license number on all advertising
- "Realtor®" must include the registered trademark symbol — not "Realtor" or "REALTOR"
- Instagram sign-off: `Loretta Sercy | Realtor® | eXp Realty | TX License #0633703`

---

## VOICE RULES

### Write this
- "Here is what the data shows."
- "This is the decision in front of you."
- "The market isn't the problem. The strategy was."
- "Before it shows up on Zillow."
- "My role is not to sell you on a house."
- "Move with Clarity. Not Pressure."

### Never this
- Any urgency or FOMO language
- Agent-centric bragging or award lists
- Generic real estate superlatives
- "Dream home" / "perfect home" / "hot market"
- Exclamation marks in body copy
- Lifestyle/acreage aesthetic language

### Voice pillars
1. **Calm authority** — precision and restraint over performance
2. **Strategic and editorial** — data with context, options with stakes
3. **Emotionally intelligent** — honors the transition, not just the transaction
4. **Transition-focused** — people move lives, not houses

---

## BRAND PERSONALITY

- **Archetype**: The Trusted Advisor — not the expert who talks down to you, but the experienced colleague who levels with you
- **If Loretta's brand were a person**: She's the calm, knowledgeable friend you call before making a major decision — not to be told what to do, but to be helped to think it through. She's been through the transition herself (city to acreage), so she speaks from experience, not theory. She's direct without being cold, warm without being effusive.
- **Core values expressed in voice**: Clarity, honesty, client protection, local knowledge, patience

---

## WE ARE / WE ARE NOT

| We Are | We Are Not |
|--------|------------|
| **Advisor** — a trusted guide who helps clients think clearly | **Salesperson** — pushing, closing, or creating urgency |
| **Calm and direct** — measured, confident, and unhurried | **Hype-driven** — exclamation points, urgency tactics, FOMO |
| **Honest and practical** — including the hard realities after closing | **Polished and vague** — generic, aspirational fluff |
| **Protective** — guarding clients' decisions and best interests | **Transactional** — focused on the deal over the person |
| **Local and specific** — deeply knowledgeable about outer DFW | **Generic** — one-size-fits-all real estate content |
| **Empathetic** — meeting clients where they are in their transition | **Condescending** — assuming clients don't know things |

---

## MESSAGING FRAMEWORK

### Primary Value Proposition
Loretta Sercy helps buyers and sellers navigate meaningful life transitions — especially from city living to acreage — with clarity, strategy, and no pressure.

### Key Message Pillars

1. **Clarity Over Pressure** — Every interaction prioritizes informed decision-making over speed or urgency. Use in all content.

2. **Life Transition Specialist** — Real estate decisions are life decisions. Use in About content, social bios, listing showcases, buyer/seller education posts.

3. **The Wave Report / East Dallas Growth Expert** — Loretta is ahead of the curve on what's happening east of Dallas. Use in market updates, location-specific posts, community spotlights.

4. **Acreage + Lifestyle Living** — Specialization in acreage, barndominiums, horse properties, and lifestyle-fit homes.

5. **Straight Talk / Real Estate Unfiltered** — Honest deal stories, negotiation strategy, and market realities other agents won't share.

### Competitive Positioning
- vs. Traditional agents: Loretta leads with lifestyle fit, not transaction speed
- vs. Big-box teams: Personal, local, specific — not a pipeline
- vs. Status quo (not buying): *"Life doesn't wait for the perfect interest rate."*

---

## TONE-BY-CONTEXT MATRIX

Voice is constant. Tone flexes by context.

| Context | Formality | Energy | Technical Depth | Key Principle |
|---------|-----------|--------|-----------------|---------------|
| Instagram Reels / video | Low | Medium | Low | Hook with a question or observation; end with engagement prompt |
| Instagram static posts | Low-Medium | Medium | Low-Medium | Punchy, specific, story-driven |
| Property showcases | Low | Medium-High | Low | Paint the life, not the specs |
| Wave Report / market updates | Low-Medium | Medium | Medium | Teach something they can't Google |
| Real Estate Unfiltered | Low | Medium | Medium | Be honest about what actually happened |
| Email outreach / follow-up | Medium | Medium | Low-Medium | Personal, helpful, no pressure |
| Website copy | Medium | Low-Medium | Low-Medium | Clear, advisory, trust-building |
| Listing descriptions | Medium | Medium | Medium | Specific details + lifestyle narrative |

### Instagram guidelines
- **Format**: Short paragraphs, heavy line breaks, one idea per paragraph
- **Opening**: Hook with observation, question, or surprising fact — never start with "I"
- **Closing**: End with a question to drive comments OR a clear CTA
- **Sign-off**: `Loretta Sercy | Realtor® | eXp Realty | TX License #0633703`
- **Hashtags**: Always include `#MoveWithClarity` + 2-4 relevant tags
- **Emoji**: Minimal — only where it adds meaning (🌊 for Wave Report, 🌳 for acreage/lifestyle)
- **Exclamation marks**: Maximum one per post

---

## TERMINOLOGY GUIDE

### Must-Use Terms
| Term | Usage | Instead Of |
|------|-------|------------|
| Move with Clarity | Tagline — use consistently | Any other version |
| Advisor | How Loretta refers to her role | Agent (when possible) |
| Life transition | What clients are navigating | "buying/selling" alone |
| Lifestyle-fit | Describing property match to life | "perfect home" |
| The Wave / Wave Report | Her market trend content series | "market update" |

### Avoid These Terms
| Term | Reason |
|------|--------|
| Dream home / Perfect home | Overused, vague, sets unrealistic expectations |
| Don't miss out / Act fast | Pressure tactics — contradicts brand promise |
| Hot market / Crazy market | Hype language |
| Easy / Simple | Minimizes complexity of client decisions |

---

## CONTENT SERIES

1. **The Wave Report** — Market intelligence on East Dallas growth. Weekly or bi-weekly.
2. **Real Estate Unfiltered** — Honest deal stories. 1-2x per month.
3. **Property Showcases** — Lifestyle-led listing content. As listings come available.
4. **Behind the Scenes** — Human, light, relatable. Occasional.
5. **Philosophy / Mindset** — Clarity-over-pressure content. 2-4x per month.

---

## THREE BUILD RULES

1. **When in doubt, add space.** Default to more white space, less color, simpler layout.
2. **Flag generic copy. Don't fill it.** If it feels generic, stop and flag it.
3. **Smarter, not just prettier.** If a decorative element doesn't make the reader feel smarter — remove it.

---

## START OF EVERY LORETTA BUILD

```
Read LORETTA BRAND.md.
Scheme: Slate & Fog.
Fonts: DM Serif Display + DM Sans.
Base file: loretta_template_base.html (C:\Veritas\assets\loretta\).
Voice: calm authority, advisor energy, transition-focused.
Three rules: space > decoration, flag generic copy, smarter not prettier.
```

---

## FILE REFERENCES

| File | Location |
|---|---|
| `LORETTA_BRAND.md` | `C:\Veritas\assets\loretta\` — original source |
| `loretta-sercy-brand-voice-guidelines.md` | `C:\Veritas\assets\loretta\` — original source |
| `loretta_template_base.html` | `C:\Veritas\assets\loretta\` — base HTML template for all builds |
| `movewithclarity_brandkit_slate.html` | `C:\Veritas\assets\loretta\` — full visual brand kit |
