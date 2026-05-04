# CLAUDE.md — Alan OS Master State
Last updated: 2026-05-03

## Prime Directive
Read this file silently. Do not summarize it back. Do not check in.
State environment, read relevant context files, execute the objective.

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

## Execution Rules
- Assume YES on all non-destructive decisions
- Do not pause for confirmation unless permanent deletion or credential exposure
- Do not ask clarifying questions — make a decision and state your assumption
- Run to completion — report final state and commit hash
- Never summarize CLAUDE.md back to the user

## Open Items
| # | Item | Blocker | Owner |
|---|------|---------|-------|
| 1 | Job Search Brief 1PyDF update | LinkedIn live — ready | Claude Code |
| 2 | n8n API key rotation | Manual — rotate in n8n UI | Alan |
| 3 | WF4.1 writeback spot-check | MMM Prospect Tracker WA tab row 2 | Alan |
| 4 | Netlify site rename | Optional cosmetic | Alan |
| 5 | Gmail OAuth redirect_uri_mismatch | Google Cloud Console fix | Alan |
| 6 | Veritas waitlist pages | Need domain decision first | Planning |
| 7 | Veritas website custom domain | Point veritasaipartners.com to Netlify | Alan |
| 8 | SalesOS architecture build | After waitlist rule met | Queued |
| 9 | Ruflo eval | Test branch ruflo-eval — in progress | Claude Code |
| 10 | Ruflo content post | LinkedIn — ready to write | Claude Code |

## Session Protocol
Open: state environment (Host or VM)
      paste Drive URL:
      https://docs.google.com/document/d/1oGKgcM6vlHS6i6kFUPx1LVBn3PW9ghUk02nR0Dcqm38/edit
Close: python scripts/post_closeout_to_drive.py
