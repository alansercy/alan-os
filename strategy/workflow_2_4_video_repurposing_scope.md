# Workflow 2.4 — Video Repurposing Scope

**Date:** 2026-04-26
**Status:** Scoped, not built
**Owner:** Loretta (MoveWithClarity / Roots & Room)

## API Availability — YES, public

Opus Clip API documented at https://help.opus.pro/api-reference/overview. Not closed beta.

| Aspect | Detail |
|---|---|
| Auth | API key from dashboard (clip.opus.pro → bottom-left corner) |
| Pricing | Credit system: 1 credit = 1 minute of video processed. API pricing not published — must contact sales for quote |
| Rate limits | 30 req/min per key, 50 concurrent projects |
| Input | URLs from YouTube, Google Drive, Vimeo, Zoom, Twitch, Facebook, X, S3 MP4. Up to 10 hr / 30 GB |
| Output | Clip URLs, metadata, timing markers. XML export for Premiere/DaVinci |
| Async | Webhook callback when project finishes — needed since processing takes minutes |
| Endpoints | Create Project, Query Clips, Share Project, Social Posting, Webhook config |

## Pre-build Requirements

1. **Account + paid plan** — confirm Loretta's current Opus Clip tier supports API access. Free trial may not.
2. **API key** — Loretta generates from dashboard, hands to me. Add to n8n as credential type `httpHeaderAuth` (Opus uses a header — confirm header name during build, likely `Authorization` or `X-API-Key`).
3. **Webhook public URL** — n8n needs a public-reachable webhook for the callback. Two options:
   - Activate n8n cloud webhook URL (production webhook URLs work if n8n is publicly reachable)
   - Cloudflare Tunnel to localhost:5678 (already exists? Check)
4. **Buffer account** — confirm subscription tier supports IG Reels + YouTube Shorts posting via API. Buffer's Publish API requires their Business plan ($60–100/mo).

## Workflow architecture (proposed)

```
[Drive folder watch]              [Opus Clip status]            [Buffer post]
  edited video uploaded             webhook callback              one per clip
  →                                 →                             →
[Trigger]  →  [POST clip-projects]  →  [Wait]  →  [GET clips]  →  [Format captions]  →  [POST to Buffer]  →  [Log to Sheet]
                                                                                                              ↓
                                                                                                       [SMS Loretta on done]
```

### Nodes

1. **Google Drive Trigger** — watch folder "Loretta — Edited for Repurposing"
2. **HTTP Request** — POST to Opus Clip /clip-projects with the Drive video URL (or download → re-upload to S3 if Drive URLs aren't supported)
3. **Webhook receiver** — separate workflow that catches the Opus completion callback and writes the project_id + clip URLs to a shared sheet
4. **Wait node** OR resume-from-webhook pattern — n8n's `$execution.resumeUrl` lets the workflow pause until Opus pings back
5. **HTTP Request** — GET clips for the project, parse URLs and timing
6. **Code** — generate captions with Claude based on Opus's auto-caption + Loretta's brand voice
7. **HTTP Request to Buffer** — schedule each clip for IG Reels and YouTube Shorts (Buffer node exists in n8n: `n8n-nodes-base.buffer`? Check — may not be native, fallback to httpRequest)
8. **Append to Content Calendar** sheet
9. **SMS Loretta** (reuse 2.3's Twilio cred when ready)

## Open questions before build

1. **Plan tier check** — does Loretta's Opus Clip plan include API access? If not, what's the upgrade cost?
2. **Aspect ratio** — Reels (9:16) only? Or also 1:1 for IG feed and 16:9 for YouTube long-form repost? Opus reframes per project, so each platform may need a separate project.
3. **Caption style** — does Loretta have a brand voice guide for captions? `strategy/lollie_brand.md` may have it.
4. **Buffer plan** — verify subscription level. If not on Business, swap to direct Meta Graph API + YouTube Data API (more setup, no monthly fee).
5. **Approval gate** — Loretta reviews clips before posting? Or full auto? Recommend gate: write to Sheet "Pending Review" status, only post after she flips to "Approved". Mirrors 3.1's draft-approval pattern.

## Estimated build time

~4–6 hours after creds + plan confirmations. Most risk is in:
- Webhook callback wiring with n8n's resume-on-webhook pattern
- Buffer API quirks (rate-limited, requires media upload first then post)

## Recommendation

Block on items 1, 2, 4 in Open Questions before building. Loretta to send: (a) Opus Clip plan name, (b) Buffer plan name, (c) approval-gate preference.
