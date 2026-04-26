# Run on VM AI-Server-Gen2 as user SecureAI-W11.
# Registers a Task Scheduler entry that runs `n8n start` on user logon,
# with working directory C:\Users\SecureAI-W11.

$ErrorActionPreference = 'Stop'

$taskName = 'n8n'
$workDir  = 'C:\Users\SecureAI-W11'
$user     = "$env:USERDOMAIN\$env:USERNAME"

# Resolve a launcher: prefer 'n8n.cmd' if on PATH, else fall back to 'npx n8n start'.
$n8nCmd = (Get-Command n8n -ErrorAction SilentlyContinue).Source
if (-not $n8nCmd) {
    $n8nCmd = (Get-Command n8n.cmd -ErrorAction SilentlyContinue).Source
}

if ($n8nCmd) {
    $action = New-ScheduledTaskAction -Execute $n8nCmd -Argument 'start' -WorkingDirectory $workDir
    Write-Host "Using direct launcher: $n8nCmd"
} else {
    $npxCmd = (Get-Command npx.cmd -ErrorAction SilentlyContinue).Source
    if (-not $npxCmd) { throw 'Neither n8n nor npx found on PATH. Install n8n first.' }
    $action = New-ScheduledTaskAction -Execute $npxCmd -Argument 'n8n start' -WorkingDirectory $workDir
    Write-Host "Using npx launcher: $npxCmd"
}

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $user
# Keep the n8n process alive — no idle stop, no exec time limit.
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RestartCount 3
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Highest

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force | Out-Null

# Verify
$t = Get-ScheduledTask -TaskName $taskName
"=== Registered ==="
"TaskName : $($t.TaskName)"
"State    : $($t.State)"
"User     : $(($t.Principal).UserId)"
"Action   : $(($t.Actions[0]).Execute) $(($t.Actions[0]).Arguments)"
"WorkDir  : $(($t.Actions[0]).WorkingDirectory)"
"Trigger  : $(($t.Triggers[0]).GetType().Name)"

# Optional: kick it off now to verify the action runs cleanly.
# Comment out if you don't want a second n8n instance racing.
"`n=== Starting now (Ctrl-C cancels) ==="
Start-ScheduledTask -TaskName $taskName
Start-Sleep -Seconds 3
Get-ScheduledTask -TaskName $taskName | Get-ScheduledTaskInfo |
    Select-Object LastTaskResult, LastRunTime, NextRunTime
