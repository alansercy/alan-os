"""Veritas Build Log — append session ship-notes to Loretta Content Calendar.

Pattern 7 from memory-bank/VIE_PATTERN_ACTION_LIST.md (build-log-as-marketing).
Every session that ships something post-worthy gets a row here. Loretta's
content engine reads from this tab as a second feed alongside the existing
Content Calendar tab — zero extra effort to surface Veritas build activity
into LinkedIn cadence.

Usage:
  python scripts/build_log.py init
  python scripts/build_log.py append \\
      --repo alan-os --head <hash> \\
      --shipped "<1-2 sentences>" \\
      --post-candidate Y \\
      --draft "<3-sentence post>" \\
      --status draft

Auth (mirrors add_tracker_columns.py pattern):
  1. Service account: C:/Users/aserc/.lux/credentials/service_account.json
  2. OAuth fallback: C:/Users/aserc/.lux/google_oauth_token.json
     (auto-refreshes via refresh_token; client secrets at
      C:/Users/aserc/.lux/google_client_secrets.json for first-time login)

Tab schema (8 cols):
  Date | Repo | HEAD | What shipped | Post candidate | Draft | Status | Posted at
"""

import argparse
import json
import os
import sys
from datetime import datetime

SHEET_ID = "1D7krpNO3CmuZBWfy_bN3c26FUvnv2y3JJ2gQGwRgyXM"
TAB_NAME = "Veritas Build Log"
HEADERS = [
    "Date",
    "Repo",
    "HEAD",
    "What shipped",
    "Post candidate",
    "Draft",
    "Status",
    "Posted at",
]

LUX_DIR = os.path.join(os.path.expanduser("~"), ".lux")
SA_PATH = os.path.join(LUX_DIR, "credentials", "service_account.json")
OAUTH_TOKEN = os.path.join(LUX_DIR, "google_oauth_token.json")
CLIENT_SECRETS = os.path.join(LUX_DIR, "google_client_secrets.json")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_client():
    try:
        import gspread
        from google.oauth2.service_account import Credentials as SACreds
        from google.oauth2.credentials import Credentials as OAuthCreds
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError as e:
        sys.exit(f"missing package: {e}\nrun: pip install gspread google-auth google-auth-oauthlib")

    if os.path.exists(SA_PATH):
        try:
            creds = SACreds.from_service_account_file(SA_PATH, scopes=SCOPES)
            client = gspread.authorize(creds)
            client.open_by_key(SHEET_ID)
            print(f"auth: service account ({SA_PATH})")
            return client
        except Exception as e:
            print(f"auth: service account failed ({e}); falling back to OAuth")

    creds = None
    if os.path.exists(OAUTH_TOKEN):
        with open(OAUTH_TOKEN) as f:
            creds = OAuthCreds.from_authorized_user_info(json.load(f), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("auth: refreshing OAuth token")
            creds.refresh(Request())
            with open(OAUTH_TOKEN, "w") as f:
                f.write(creds.to_json())
        else:
            if not os.path.exists(CLIENT_SECRETS):
                sys.exit(f"no creds at {CLIENT_SECRETS}")
            print("auth: launching OAuth browser flow")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS, SCOPES)
            creds = flow.run_local_server(port=0)
            with open(OAUTH_TOKEN, "w") as f:
                f.write(creds.to_json())

    print(f"auth: OAuth ({OAUTH_TOKEN})")
    return gspread.authorize(creds)


def cmd_init():
    gc = get_client()
    sh = gc.open_by_key(SHEET_ID)
    existing = [ws.title for ws in sh.worksheets()]
    if TAB_NAME in existing:
        ws = sh.worksheet(TAB_NAME)
        current = ws.row_values(1)
        if current == HEADERS:
            print(f"tab '{TAB_NAME}' already exists with correct headers; no-op")
            return
        print(f"tab '{TAB_NAME}' exists but headers differ; current={current}")
        sys.exit("refusing to overwrite — inspect manually")
    ws = sh.add_worksheet(title=TAB_NAME, rows=1000, cols=len(HEADERS))
    ws.update(range_name="A1:H1", values=[HEADERS])
    print(f"created tab '{TAB_NAME}' with {len(HEADERS)} columns")
    print(f"sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit")


def cmd_append(args):
    gc = get_client()
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet(TAB_NAME)
    row = [
        args.date or datetime.now().strftime("%Y-%m-%d"),
        args.repo,
        args.head,
        args.shipped,
        args.post_candidate.upper(),
        args.draft or "",
        args.status,
        args.posted_at or "",
    ]
    ws.append_row(row, value_input_option="USER_ENTERED")
    print(f"appended row to '{TAB_NAME}': {row[:4]}")


def main():
    p = argparse.ArgumentParser(prog="build_log")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="create Veritas Build Log tab")
    a = sub.add_parser("append", help="append a row")
    a.add_argument("--date")
    a.add_argument("--repo", required=True)
    a.add_argument("--head", required=True)
    a.add_argument("--shipped", required=True)
    a.add_argument("--post-candidate", required=True, choices=["Y", "N", "y", "n"])
    a.add_argument("--draft", default="")
    a.add_argument("--status", default="draft", choices=["draft", "queued", "posted", "skipped"])
    a.add_argument("--posted-at", default="")
    args = p.parse_args()
    if args.cmd == "init":
        cmd_init()
    elif args.cmd == "append":
        cmd_append(args)


if __name__ == "__main__":
    main()
