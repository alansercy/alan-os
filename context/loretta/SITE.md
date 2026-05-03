# Loretta Site — Current State

## Hosting
- **Live host:** SiteGround GrowBig WordPress (shared with Veritas on same SiteGround account)
- **Domain:** lorettasercy.com
- **Brand:** MoveWithClarity — "Move with Clarity. Not Pressure."

## DNS Status
- Currently pointed at Lofty (IDX platform)
- Cutover to SiteGround happens at W1 session close
- Do not touch DNS until W1 is confirmed ready

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
