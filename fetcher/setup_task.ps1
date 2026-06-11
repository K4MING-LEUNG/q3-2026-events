# Register Windows Scheduled Task: daily 08:00 news fetch for Q3 2026 site.

$TaskName = "Q3SiteDailyNews"
$ScriptDir = $PSScriptRoot
$BatPath = Join-Path $ScriptDir "run.bat"

if (-not (Test-Path $BatPath)) {
    Write-Error "run.bat not found at $BatPath"
    exit 1
}

schtasks /Query /TN $TaskName 2>$null | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Removing existing task $TaskName..."
    schtasks /Delete /TN $TaskName /F | Out-Null
}

schtasks /Create `
    /TN $TaskName `
    /TR "`"$BatPath`"" `
    /SC DAILY `
    /ST 08:00 `
    /F | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Task '$TaskName' registered: daily 08:00"
    Write-Host "Run now : schtasks /Run /TN $TaskName"
    Write-Host "Verify  : schtasks /Query /TN $TaskName /V /FO LIST"
    Write-Host "Delete  : schtasks /Delete /TN $TaskName /F"
} else {
    Write-Error "Failed to register task"
    exit 1
}
