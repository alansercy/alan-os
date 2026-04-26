# VM hand-off scripts

These scripts must be run **inside** the VM `AI-Server-Gen2` as user `SecureAI-W11`. They cannot be executed from the host because:

- VM SSH (port 22), WinRM (5985/5986), and SMB (445) are all blocked from the host (Apr 26 probe).
- Only the n8n REST API (forwarded localhost:5678) is reachable.
- PowerShell Direct (VMBus) requires the VM user's password, which is not stored on the host.

## Transfer

Copy via Hyper-V Enhanced Session clipboard, or via `vmconnect.exe`'s drag-drop, or paste each script into a PowerShell window in the VM.

## Run order

```powershell
# In VM, opened as Administrator (or any elevated PS prompt under SecureAI-W11):
Set-ExecutionPolicy -Scope Process Bypass -Force
.\01_register_n8n_autostart.ps1
.\02_add_mmm_sheets_url.ps1
```

After both succeed, sign out and back in once to confirm the n8n task starts at logon.

## What each does

- **01_register_n8n_autostart.ps1** — Registers Task Scheduler entry `n8n` that runs `n8n start` (or `npx n8n start` if `n8n` is not on PATH) at user logon, working directory `C:\Users\SecureAI-W11`. Configures restart-on-failure (3 tries, 1 min apart) and disables idle-stop. Triggers a test launch at the end.
- **02_add_mmm_sheets_url.ps1** — Locates the n8n `.env` (preference order: `C:\Users\SecureAI-W11\.n8n\.env`, then `C:\Users\SecureAI-W11\.env`, then AppData) and sets `MMM_SHEETS_URL=https://docs.google.com/spreadsheets/d/1OePOK2GaGB2JrXO5QUSrXkzceGQ8V2l4`. Updates in place if already present, else appends. Creates the file if no candidate exists.
