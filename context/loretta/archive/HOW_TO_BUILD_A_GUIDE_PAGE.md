# How to Build a New Guide Page
**MoveWithClarity · Loretta Sercy**
**Last updated: May 2026**

---

## What You Have

Two files:

1. **`loretta_guide_template.html`** — the blank HTML shell for every new guide page. All brand styling is locked in. You fill in content only.
2. **`BRAND_SYSTEM.md`** — your brand rules, voice guidelines, TREC compliance, and active guide briefs. Paste this into Claude at the start of every session.

---

## How to Build a New Guide Page

### Step 1 — Start a new Claude session

Paste this at the top:

> "I'm building a new MoveWithClarity guide page. Here is my brand system:"

Then paste the full contents of `BRAND_SYSTEM.md`.

Then say:

> "I'm using `loretta_guide_template.html` as my base. Here is the template code:"

Then paste the full contents of `loretta_guide_template.html`.

Then say:

> "The guide I'm building is [guide name]. Here is my brief:"

Then paste your brief (guide name, purpose, target person, emotional state, section flow, style notes).

---

### Step 2 — Ask Claude to fill the template

Say:

> "Please fill in all the `<!-- REPLACE: ... -->` sections using my brief and brand voice. Do not change the design tokens, nav, footer compliance block, or JavaScript. Output the complete filled HTML file."

---

### Step 3 — Review and refine

Claude will output a complete HTML file. Read through it and note anything that doesn't sound right. Then say:

> "Please adjust: [your notes]. Keep everything else the same."

Repeat until it sounds like you.

---

### Step 4 — Save with the right filename

Name the file after the URL slug. Examples:
- `why-your-house-didnt-sell.html`
- `divorce-housing-clarity-guide.html`
- `acreage-transition-guide.html`

---

## Things You Can Change

| What | Where in the template | How |
|---|---|---|
| Guide accent color | `:root { --accent: }` at the top of `<style>` | Change the hex value |
| Hero headline (3 lines) | `.hero-headline`, `.hero-headline-2`, `.hero-headline-3` | Edit the text |
| Eyebrow / guide label | `.hero-eyebrow`, `.hero-guide-label` | Edit the text |
| Number of sections | The `<!-- SECTION 01 -->` blocks | Add or remove section blocks |
| Section background | `class="guide-section chalk"` or `cream` | Change `chalk` to `cream` or vice versa |
| Pull quote color | `class="pull-quote accent"` | Use `accent`, `light`, or leave blank for default gold |
| Framework steps | `.fw-card` blocks | Add/remove cards, update step numbers |
| Footer guide links | `.footer-links` in the footer | Add links as new guides go live |
| CTA copy | `.gc-headline`, `.gc-body` | Edit text |
| Nav CTA | `.nav-cta` | Change button text and `href` anchor |

---

## Things You Must NOT Change

- Design tokens (the `--navy`, `--gold`, `--cream`, etc. variables)
- Font declarations (`Playfair Display`, `Jost`)
- The nav HTML structure and wordmark
- Footer compliance block (license numbers, Equal Housing, TREC disclaimer)
- The JavaScript block at the bottom
- The reading progress bar HTML

These are locked across all pages to keep the site consistent.

---

## TREC Compliance Checklist

Before publishing any page, confirm:

- [ ] No closed sale prices mentioned anywhere
- [ ] No price per acre at closing
- [ ] No specific transaction dollar amounts
- [ ] License number visible (it's in the footer — don't remove it)
- [ ] "Comps" used instead of "value" for any pricing references
- [ ] Legal disclaimer in footer is appropriate for this guide's topic

---

## Guide Accent Colors — Reference

Each guide can have a subtle accent color that gives it its own emotional feel while staying in the same family as the core palette. Set `--accent` in the `:root` block.

| Guide | Accent | Feeling |
|---|---|---|
| Parents' Move | `#9E6B52` | Warm, familial |
| Divorce & Housing | `#6B7A8F` | Calm, grounded |
| Why Your House Didn't Sell | `#8B7355` | Diagnostic, honest |
| Acreage / Lifestyle | `#B8903C` (gold — default) | Aspirational |
| New Build / First-Time | `#7A8B7A` | Fresh, careful |

You can also just leave `--accent` set to `var(--gold)` if you don't want a guide-specific feel.

---

## Footer Links — Keep Updated

As new guides go live, update the "Other Guides" links in the footer of every existing page. The list currently includes:
- The Clarity Blueprint (`/clarity-blueprint`)
- The Parents' Move Guide (`/parents-move-guide`)
- Why Your House Didn't Sell (`/why-your-house-didnt-sell`)
- Divorce & Housing Clarity (`/divorce-housing-clarity-guide`)

Alan can do a batch footer update across all pages once you have 4–5 live.

---

## When You're Done — Send Back to Alan

When a guide page is ready, send Alan:
1. The completed HTML file
2. The intended URL slug
3. Any notes on what you'd like reviewed or adjusted

He handles deployment to `lorettasercy.com`.

---

*Questions? Alan Sercy — asercy@msn.com*
