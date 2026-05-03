# CLAUDE.md — Alan OS Master State
Last updated: 2026-05-03

## Environments
HOST — personal operator + product lab (you are here)
  Code: C:\Veritas\repos\alan-os\
  Runtime: C:\Users\aserc\.lux\ (not in GitHub)
VM — SecureAI-W11 — n8n, commercial builds
  Context always sourced from Host. VM executes only.

## Task Router
Before any task, read the relevant context file(s):
| Task | Read first |
|------|------------|
| Loretta website or brand | context/loretta/BRAND.md + SITE.md |
| Loretta n8n workflows | context/loretta/WORKFLOWS.md |
| Veritas site or brand | context/veritas/BRAND.md + SITE.md |
| AgentOS | context/products/agentOS/SPEC.md |
| TradeOS | context/products/tradeOS/SPEC.md |
| SalesOS | context/products/salesOS/SPEC.md |
| PersonalOS | context/products/personalOS/SPEC.md |
| Host stack + .lux folder | context/infrastructure/HOST.md |
| VM + n8n | context/infrastructure/VM.md |
| MMM trucking | context/mmm/BD.md |
| Job search | context/job-search/STATUS.md |
| Family/estate | context/family/STEWARDSHIP.md |

## Open Items
| # | Item | Blocker | Owner |
|---|------|---------|-------|
| 1 | Job Search Brief 1PyDF update | LinkedIn live — ready | Claude Code |
| 2 | n8n API key rotation | Manual — rotate in n8n UI | Alan |
| 3 | WF4.1 writeback spot-check | MMM Prospect Tracker WA tab row 2 check Notes | Alan |
| 4 | Netlify site rename | Optional cosmetic | Alan |
| 5 | Gmail OAuth redirect_uri_mismatch | Google Cloud Console fix | Alan |
| 6 | Veritas waitlist pages | Need domain decision first | Planning |
| 7 | Veritas website custom domain | Site live at Netlify URL — need to point veritasaipartners.com | Alan |
| 8 | SalesOS architecture build | After waitlist rule met | Queued |
| 9 | Ruflo content post | LinkedIn live — ready to write | Claude Code |

## Session Protocol
Open: state environment (Host or VM)
      paste Drive URL:
      https://docs.google.com/document/d/1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38/edit
Close: python scripts/post_closeout_to_drive.py
