# Lux Stack — SOP
**Owner:** Alan Sercy
**Last Updated:** April 22, 2026
**Environment:** Host machine only — never VM

---

## Architecture

**Launcher:** `C:\Users\aserc\.lux\workflows\lux_launcher.py`
Replaced 21 individual Task Scheduler tasks with 3 unified launcher tasks.

**Key fixes applied:**
- Outlook COM timing: kill/restart + 135s wait
- Emoji encoding: `PYTHONUTF8=1`
- PowerShell patch script for multi-file rule updates

---

## Five Managed Accounts

| Account | Purpose | Script |
|---|---|---|
| asercy@msn.com | Alan personal/MSN | triage_msn.py |
| alansercy@gmail.com | Alan primary | triage_gmail.py |
| lorettasercy@gmail.com | Loretta personal | triage_loretta.py |
| loretta.keysandcommunity@gmail.com | Loretta eXp Realty | triage_keys.py |
| lsercy@mmmtrucks.com | MMM Trucking | triage_mmm.py |

---

## Norman Inbox Guard (Standalone)

**Script:** `C:\Users\aserc\.lux\norman_inbox_guard.py`
**Schedule:** Daily 6AM via Task Scheduler — "Norman Inbox Guard"
**Account:** sercypete@aol.com (Norman's AOL)
**Digest:** Sent daily to alansercy@gmail.com
**Logs:** `C:\Users\aserc\.lux\logs\norman_guard_YYYY-MM-DD.log`

### How It Works
- USAA emails → `Inbox/USAA` folder automatically
- Whitelisted senders → stay in inbox, marked unread (prevents AOL OldMail archiving)
- Everything else → `Filtered` folder silently
- Daily digest → kept/filtered/USAA summary + new sender list for whitelist review

### Whitelist File
`C:\Users\aserc\.lux\norman_whitelist.txt`
14 addresses + 2 domain rules (@penfed.org, @penfed.info)

### Forwarding to Marsha
Staged but disabled. When ready: open `norman_inbox_guard.py` → set `FORWARDING_ENABLED = True`
Marsha's address already configured as `sercymarsha@aol.com`

---

## Governance Protocol

**Trigger prefix:** `LUX UPDATE —`
Use this prefix in chat to log async governance notes without interrupting workflow.

**Session Start Protocol:**
1. Paste Google Doc URL or GitHub handoff URL
2. State Host or VM environment
3. State primary objective

**Master Handoff Doc:** Google Drive `1MOvSzYF7iV0tEICRJfforTIojYigryi6MOFDpako5xQ` (alansercy@gmail.com)
Treat as read-only during sessions — append notes only, never inline edit.

**Friday NLM sync:** Natural governance checkpoint.

---

## Open Issues

| Issue | Root Cause | Fix |
|---|---|---|
| `review_new_senders.py` COM "exhausted shared resources" | Loretta Gmail background-syncing after newly added to Outlook | Add Outlook kill/restart block + wait for full sync before re-testing |
| Claude Usage Dashboard bat file | `set ANTHROPIC_ADMIN_API_KEY=` line malformed | Fix set line format, rotate key |

---

## Claude Usage Dashboard

**Running at:** localhost:8081
**Script:** `C:\Users\aserc\.lux\claude_usage_dashboard.py`
**UI:** `C:\Users\aserc\.lux\claude_usage_dashboard.html`
**Bat file:** `C:\Users\aserc\.lux\start_alan_os.bat`
**Pending:** Fix bat file key, add Norman AOL inbox, add manual run button

---

## Environment Rules

- **Host machine:** Personal + Veritas work ONLY
- **VM (SecureAI-W11):** AgentOS + n8n development ONLY
- Never cross the boundary
