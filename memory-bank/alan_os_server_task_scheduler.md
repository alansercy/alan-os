# AlanOS_Server — Task Scheduler config

**Status:** ✅ Live | **Verified:** 2026-05-02 | **Repo:** alan-os (this file) — task itself lives in Windows Task Scheduler on host

The Alan OS dashboard server (`alan_os_server.py`, port 8000) auto-starts via a Task Scheduler entry that already exists on Alan's host machine. This note captures the exact config so it can be re-created if the task is ever deleted or the host is rebuilt.

## Config (as registered)

| Field | Value |
|---|---|
| Task name | `\AlanOS_Server` |
| Description | `Alan OS auto-start` |
| Trigger | At logon time |
| Run as | `aserc` (LogonType: InteractiveToken) |
| Action — Program | `C:\Python314\python.exe` |
| Action — Arguments | `"C:\Users\aserc\.lux\workflows\alan_os_server.py"` |
| Action — Start In | `C:\Users\aserc\.lux\workflows` |
| Hidden | true |
| Execution time limit | none (PT0S — runs indefinitely) |
| Multiple instances policy | IgnoreNew |
| Restart on failure | 3 attempts × 2-minute intervals |
| Scheduling engine | UseUnifiedSchedulingEngine = true |

## Why logon (not boot)

The server backs the dashboard at `localhost:8000/dashboard`, which Alan only uses while signed in. Boot-trigger would start the process before the desktop session exists, with no consumer. Logon-trigger ties lifecycle to Alan's session — server up when he's working, down when he's not.

If a true boot-trigger is ever needed (e.g. for cron-like background jobs that must run regardless of login state), add a second `OnBoot` trigger to the same task — don't replace the logon trigger.

## Recreate-from-scratch command

Run from elevated PowerShell on the host:

```powershell
$action = New-ScheduledTaskAction `
    -Execute "C:\Python314\python.exe" `
    -Argument '"C:\Users\aserc\.lux\workflows\alan_os_server.py"' `
    -WorkingDirectory "C:\Users\aserc\.lux\workflows"

$trigger = New-ScheduledTaskTrigger -AtLogOn -User "aserc"

$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Seconds 0) `
    -MultipleInstances IgnoreNew `
    -Hidden

$principal = New-ScheduledTaskPrincipal `
    -UserId "aserc" `
    -LogonType Interactive

Register-ScheduledTask `
    -TaskName "AlanOS_Server" `
    -Description "Alan OS auto-start" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal
```

## Operational notes

- **Restart pattern** (used in 2026-05-01 PM session for `/model-usage` endpoint deploy):
  ```powershell
  Stop-ScheduledTask -TaskName AlanOS_Server
  Start-ScheduledTask -TaskName AlanOS_Server
  ```
  Wait ~5s after start before hitting the API.
- **Verify running**: `schtasks /Query /TN "AlanOS_Server" /V /FO LIST` — `Status: Running` and `Last Result: 267009` (= `0x41301`, "task is currently running"; not an error).
- **Check it's actually serving**: `curl http://localhost:8000/digest` or open `localhost:8000/dashboard`.
- **Logs**: `alan_os_server.py` writes to stdout — Task Scheduler captures nothing by default. If you need run logs, add `-RedirectStandardOutput` to the action or wrap the call in a `.bat` that tees to a logfile.

## Related

- Server source: `C:\Users\aserc\.lux\workflows\alan_os_server.py` (lux-os repo)
- Dashboard UI: `C:\Users\aserc\.lux\dashboard\index.html` (lux-os repo)
- Manual start fallback: `C:\Users\aserc\.lux\start_alan_os.bat`
