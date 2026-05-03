# Loretta Site — Current State
Last updated: 2026-05-03 (Session H)

## Hosting
- **Live host:** SiteGround GrowBig WordPress — **WordPress 6.9.4 installed** (shared with Veritas on same SiteGround account)
- **Domain:** lorettasercy.com
- **Brand:** MoveWithClarity — "Move with Clarity. Not Pressure."
- **Staging:** staging2.lorettasercy.com (environment name: loretta-build) — created Session H

## DNS Status
- **A records added:** lorettasercy.com + staging2.lorettasercy.com → `8.230.105.83`
- **Nameservers:** still at Lofty/Cloudflare — propagating as of 2026-05-03
- Do not treat DNS as live until staging2.lorettasercy.com/wp-admin is accessible
- Lofty IDX DNS cutover still deferred to L2

## W1 Session Status
- **W1 not started** — blocked on staging2.lorettasercy.com/wp-admin access (DNS propagation)
- **Brand audit complete (Session H)** — tokens reconciled, naming decisions locked (see BRAND.md)
- Once staging wp-admin is accessible: proceed with W1 WordPress shell build

## W1 Session Scope
Build WordPress shell only:
- Brand config (colors, fonts, Roots & Room theme)
- Page stubs: Home, About, Guides, Contact
- No Lofty IDX integration in W1
- No content migration in W1

## Lofty IDX
- Required for property search functionality
- Integration scoped to **L2 session** (not W1)
- Lofty is current DNS destination — do not cut over until IDX is wired in L2

## HTML Prototype
- **Location:** `C:\Users\SecureAI-W11\Projects\loretta-site\` — this path exists on the VM (SecureAI-W11), not the Host
- Files found at that path on Host: NOT FOUND (VM-resident path)
- HTML assets available on Host at: `C:\Veritas\assets\loretta\`
  - `lorettasercy_homepage_slate.html` — homepage prototype
  - `movewithclarity_brandkit_slate.html` — full visual brand kit
  - `loretta_template_base.html` — base build template
  - `wave-report-landing-page.html` — Wave Report landing page

## Session Queue
| Session | Scope |
|---------|-------|
| W1 | WordPress shell, brand config, page stubs — no Lofty |
| L2 | Lofty IDX integration, DNS cutover |
| L3 | ManyChat RELIST trigger, first nurture sequence |
