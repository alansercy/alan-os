# Run on VM AI-Server-Gen2 as user SecureAI-W11.
# Adds (or updates) MMM_SHEETS_URL in the n8n .env file at C:\Users\SecureAI-W11\.n8n\.env.
# If the .env file doesn't exist there, the script reports candidate locations.

$ErrorActionPreference = 'Stop'

$value = 'https://docs.google.com/spreadsheets/d/1RolDt3XhkV0ZkPgBdywBCCBR2R1v042V5fuZXoYplzI'
$line  = "MMM_SHEETS_URL=$value"

$candidates = @(
    'C:\Users\SecureAI-W11\.n8n\.env',
    'C:\Users\SecureAI-W11\.env',
    'C:\Users\SecureAI-W11\AppData\Roaming\n8n\.env'
)

$target = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $target) {
    Write-Host "No existing .env found. Creating: $($candidates[0])"
    $target = $candidates[0]
    New-Item -Path (Split-Path $target -Parent) -ItemType Directory -Force | Out-Null
    Set-Content -Path $target -Value $line -Encoding UTF8
    "WROTE NEW: $target"
    "VALUE   : $line"
    return
}

Write-Host "Editing: $target"
$content = Get-Content $target -Raw
if ($content -match '(?m)^MMM_SHEETS_URL=.*$') {
    $new = [regex]::Replace($content, '(?m)^MMM_SHEETS_URL=.*$', $line)
    Set-Content -Path $target -Value $new -Encoding UTF8 -NoNewline
    "UPDATED existing line in: $target"
} else {
    Add-Content -Path $target -Value "`r`n$line" -Encoding UTF8
    "APPENDED new line to: $target"
}

# Verify
"`n=== Current MMM_SHEETS_URL line ==="
Select-String -Path $target -Pattern '^MMM_SHEETS_URL=' | ForEach-Object { $_.Line }

"`nReminder: restart n8n for the new env var to take effect (the scheduled task created by 01_register_n8n_autostart.ps1 picks it up at next launch)."
