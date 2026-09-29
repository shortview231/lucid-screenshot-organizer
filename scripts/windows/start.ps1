$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Python = Join-Path $RepoRoot ".venv\Scripts\python.exe"

$TesseractCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Tesseract-OCR"),
    (Join-Path $env:ProgramFiles "Tesseract-OCR")
)
foreach ($Candidate in $TesseractCandidates) {
    if (Test-Path (Join-Path $Candidate "tesseract.exe")) {
        if (($env:Path -split ";") -notcontains $Candidate) {
            $env:Path = "$Candidate;$env:Path"
        }
        break
    }
}

& $Python -m lucid_screenshot_organizer.main
