$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Venv = Join-Path $RepoRoot ".venv"
$Python = Join-Path $Venv "Scripts\python.exe"
$StartScript = Join-Path $RepoRoot "scripts\windows\start.ps1"
$ConfigDir = Join-Path $env:LOCALAPPDATA "lucid-screenshot-organizer"
$ConfigPath = Join-Path $ConfigDir "config.toml"

$UsePyLauncher = $false
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3.11 -c "import sys" 2>$null
    $UsePyLauncher = ($LASTEXITCODE -eq 0)
}

if ($UsePyLauncher) {
    py -3.11 -m venv $Venv
} else {
    $PythonCommand = Get-Command python -ErrorAction SilentlyContinue
    if (-not $PythonCommand) {
        throw "Python 3.11+ was not found. Install Python 3.11+ first."
    }
    & $PythonCommand.Source -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)"
    if ($LASTEXITCODE -ne 0) {
        throw "Python 3.11+ is required."
    }
    & $PythonCommand.Source -m venv $Venv
}
& $Python -m pip install --upgrade pip
& $Python -m pip install -e $RepoRoot

New-Item -ItemType Directory -Force -Path $ConfigDir | Out-Null
if (-not (Test-Path $ConfigPath)) {
    Copy-Item (Join-Path $RepoRoot "config\config.example.toml") $ConfigPath
}

$PowerShell = (Get-Command powershell.exe -ErrorAction Stop).Source
$Action = New-ScheduledTaskAction -Execute $PowerShell -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$StartScript`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Days 3650)
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "Lucid Screenshot Organizer" -Action $Action -Trigger $Trigger -Settings $Settings -Principal $Principal -Force | Out-Null

Write-Host "Installed Lucid Screenshot Organizer."
Write-Host "Config: $ConfigPath"
Write-Host "Run now with:"
Write-Host "  & '$Python' -m lucid_screenshot_organizer.main"
