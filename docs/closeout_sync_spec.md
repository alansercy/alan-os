> STATUS: COMPLETE — all 4 OAuth/Drive steps done 4/30/2026, token cached at credentials/gdocs_host_token.json, post_closeout_to_drive.py running silently as of 5/2/2026.

# Closeout Sync — Spec
# Goal: auto-POST CLOSEOUT.md to Google Doc at session end

## What it does
At session end, post_closeout_to_drive.py appends CLOSEOUT.md
to the Veritas Session Log Google Doc so Claude.ai can fetch
full context via Drive MCP — no manual paste required.

## Files
- scripts/post_closeout_to_drive.py
- .lux/.env — add VERITAS_SESSION_LOG_DOC_ID=<doc_id>
- C:\Users\aserc\.lux\credentials\gdocs_host_client.json

## Build order
1. Create Google Doc "Veritas Session Log" in alansercy@gmail.com,
   get doc ID, add VERITAS_SESSION_LOG_DOC_ID to .lux/.env
2. Download OAuth 2.0 client JSON from GCP project 422640626939
   → APIs & Services → Credentials → save to
   C:\Users\aserc\.lux\credentials\gdocs_host_client.json
3. Write scripts/post_closeout_to_drive.py:
   - Load VERITAS_SESSION_LOG_DOC_ID from .lux/.env
   - Read CLOSEOUT.md from repo root
   - Auth via OAuth (cache token at gdocs_host_token.json)
   - Append dated section header + full CLOSEOUT.md content
   - Print: "Synced to Veritas Session Log — [url]"
   - Non-fatal on failure — never block session close
4. pip install --break-system-packages google-auth
   google-auth-oauthlib google-api-python-client
5. Run once for OAuth browser flow — pause here for my input
6. Test: confirm append landed in Google Doc
7. Add to SESSION_PROTOCOL.md closeout section:
   "5. Run: python scripts/post_closeout_to_drive.py"
8. Commit and push
