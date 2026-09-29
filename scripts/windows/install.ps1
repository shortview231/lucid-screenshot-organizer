$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Venv = Join-Path $RepoRoot ".venv"
$Python = Join-Path $Venv "Scripts\python.exe"
$ConfigDir = Join-Path $env:LOCALAPPDATA "lucid-screenshot-organizer"
$ConfigPath = Join-Path $ConfigDir "config.toml"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' was not found. Install Python 3.11+ first."
}

py -3.11 -m venv $Venv
& $Python -m pip install --upgrade pip
& $Python -m pip install -e $RepoRoot

New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
if (-not (Test-Path $ConfigPath)) {
    Copy-Item (Join-Path $RepoRoot "config\config.example.toml") $ConfigPath
}

$Action = New-ScheduledTaskAction -Execute $Python -Argument "-m lucid_screenshot_organizer.main"
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Days 3650)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "Lucid Screenshot Organizer" -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null

Write-Host "Installed Lucid Screenshot Organizer."
Write-Host "Config: $ConfigPath"
Write-Host "Run now with:"
Write-Host "  & '$Python' -m lucid_screenshot_organizer.main"