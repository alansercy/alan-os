#!/usr/bin/env python3
"""
post_closeout_to_drive.py

Append CLOSEOUT.md to the Veritas Session Log Google Doc at session close so
claude.ai sessions can fetch full context via Drive MCP without manual paste.

Non-fatal: any failure prints a warning to stderr and exits 0 — never blocks
session close.

Usage:  python scripts/post_closeout_to_drive.py
Spec:   docs/closeout_sync_spec.md
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path

LUX_ENV         = Path(r"C:\Users\aserc\.lux\.env")
CREDS_PATH      = Path(r"C:\Users\aserc\.lux\credentials\gdocs_host_client.json")
TOKEN_PATH      = Path(r"C:\Users\aserc\.lux\credentials\gdocs_host_token.json")
DOC_ID_KEY      = "VERITAS_SESSION_LOG_DOC_ID"
REPO_ROOT       = Path(__file__).resolve().parent.parent
CLOSEOUT_PATH   = REPO_ROOT / "CLOSEOUT.md"
SCOPES          = ["https://www.googleapis.com/auth/documents"]


def warn(msg: str) -> None:
    print(f"[closeout-sync] WARN: {msg} — session close not blocked", file=sys.stderr)


def load_dotenv(path: Path) -> dict:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get_credentials():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        if not CREDS_PATH.exists():
            raise FileNotFoundError(
                f"OAuth client JSON missing at {CREDS_PATH}. "
                "Download from GCP Console > APIs & Services > Credentials."
            )
        flow  = InstalledAppFlow.from_client_secrets_file(str(CREDS_PATH), SCOPES)
        creds = flow.run_local_server(port=0)
    TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    return creds


def append_to_doc(doc_id: str, content: str) -> None:
    from googleapiclient.discovery import build

    creds   = get_credentials()
    service = build("docs", "v1", credentials=creds)
    doc     = service.documents().get(documentId=doc_id).execute()
    end_idx = doc["body"]["content"][-1]["endIndex"] - 1
    service.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {"insertText": {"location": {"index": end_idx}, "text": content}},
            ],
        },
    ).execute()


def main() -> int:
    try:
        env    = load_dotenv(LUX_ENV)
        doc_id = env.get(DOC_ID_KEY) or os.environ.get(DOC_ID_KEY)
        if not doc_id:
            warn(f"{DOC_ID_KEY} not set in {LUX_ENV}")
            return 0
        if not CLOSEOUT_PATH.exists():
            warn(f"{CLOSEOUT_PATH} not found")
            return 0

        body    = CLOSEOUT_PATH.read_text(encoding="utf-8")
        stamp   = datetime.now().strftime("%Y-%m-%d %H:%M")
        divider = "=" * 25
        section = f"\n\n{divider}\nCLOSEOUT — {stamp}\n{divider}\n\n{body}\n"

        append_to_doc(doc_id, section)
        print(f"Synced to Veritas Session Log — https://docs.google.com/document/d/{doc_id}/edit")
        return 0
    except Exception as e:
        warn(str(e))
        return 0


if __name__ == "__main__":
    sys.exit(main())
