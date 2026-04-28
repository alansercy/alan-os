# Workflow 2.4 — Video Repurposing (Loretta Sercy)
**Status:** Ready to import  
**n8n instance:** https://n8n.lorettasercy.com  
**Google Sheet:** `1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM`

---

## Pre-Deployment Checklist

### 1. Environment Variables (set in n8n Settings → Environment)
| Variable | Value |
|---|---|
| `OPUS_CLIP_API_KEY` | API key from https://opus.pro → Settings → API |
| `BUFFER_ACCESS_TOKEN` | OAuth token from https://buffer.com/developers/apps |
| `BUFFER_PROFILE_IDS` | Comma-separated Buffer profile IDs for Loretta's accounts (Instagram, TikTok, Facebook) |

To find Buffer profile IDs: `GET https://api.bufferapp.com/1/profiles.json?access_token=YOUR_TOKEN`

### 2. Google Sheets Credential
- Open the workflow in n8n
- On both `Google Sheets: Log Success` and `Google Sheets: Log Error` nodes, replace `PLACEHOLDER_GOOGLE_SHEETS` with an active Google Sheets credential
- The credential needs access to Loretta's Content Tracker sheet
- Expected to use one of the existing `google_cred_1/2/3` credentials in n8n — reauth those first per DIRECTIVE.md

### 3. Google Sheet Setup
The sheet `Video Log` must exist in the target spreadsheet with these columns in row 1:
```
Date | Video Title | Clips Generated | Platforms | Status | Buffer Response | Submitted At
```
Create this tab if it doesn't exist.

---

## Trigger Methods

### Manual (via n8n UI)
Click "Execute Workflow" — prompts for no inputs; set `video_url` and `video_title` by editing the Manual Trigger or injecting via the Set node.

### Webhook (automated)
POST to: `https://n8n.lorettasercy.com/webhook/video-repurpose`

```json
{
  "video_url": "https://example.com/path/to/video.mp4",
  "video_title": "Q2 Market Update — April 2026",
  "platforms": "instagram,tiktok,facebook"
}
```

`platforms` is optional — defaults to `instagram,tiktok,facebook` if omitted.

This webhook can be called from:
- A file-upload form
- A Zapier/Make automation watching a Google Drive folder
- A local script monitoring a video drop folder

---

## Flow Summary

```
Trigger (manual or webhook)
  → Normalize input fields
  → POST /v1/projects to Opus Clip (submits video for AI clipping)
  → Store job context (project_id, title, platforms)
  → Wait 5 minutes (Opus Clip processing time)
  → GET /v1/projects/{id} to check status
  → IF status == "complete":
      YES → iterate each clip →
              POST to Buffer API (schedules short-form post per platform)
              (loop until all clips scheduled)
            → Append success row to Google Sheet
      NO  → Append failure row to Google Sheet (includes project_id for manual retry)
```

---

## Opus Clip API Notes
- Endpoint: `https://api.opus.pro/v1/projects`
- Requests up to 5 clips per video (`num_clips: 5`)
- Resolution: 1080p, Language: en
- Average processing time: 3–8 min depending on video length
- If a video is longer than 60 min, increase Wait node to 10–15 min
- Clips array in the status response: `response.clips[].url` and `response.clips[].title`

**If Opus Clip job is not done after 5 min wait:** The error path logs the project_id to the sheet. Loretta or an operator can manually re-trigger with that project_id — or the Wait node duration can be increased.

---

## Buffer Scheduling Notes
- Posts are queued (not posted immediately) — Buffer distributes them across Loretta's schedule
- To post immediately, change the `now` body parameter to `true`
- The caption appends `#realestate #lorettasercy #realtor` — edit in `HTTP: Schedule in Buffer` node
- `BUFFER_PROFILE_IDS` must list all target profiles; Buffer requires at least one

---

## Import Instructions
1. In n8n: Workflows → Import from File → select `workflow_2_4_video_repurposing.json`
2. Set environment variables (see above)
3. Swap `PLACEHOLDER_GOOGLE_SHEETS` credential on both Sheets nodes
4. Verify the `Video Log` tab exists in the sheet
5. Run a test with a short MP4 URL before activating
6. Set workflow to **Active** to enable the webhook trigger

---

## Known Limitations
- Single poll attempt after fixed 5-min wait — no retry loop (by design; keeps workflow simple)
- Buffer API v1 (`bufferapp.com`) — if Buffer migrates to Publish API v2, update the URL
- Clip extraction from `response.clips[]` assumes Opus Clip's standard response shape; verify against their current API docs on first run
