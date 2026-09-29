# Lucid Screenshot Organizer

Local-first screenshot organization for Windows 11 and Pop!_OS Linux.

Features:
- Watches the platform screenshot folder.
- Uses local OCR when Tesseract is available.
- Renames screenshots with timestamp plus a short OCR-derived label.
- Sorts into Year / Month / Day folders.
- Never overwrites an existing file.
- Falls back to timestamp naming when OCR is unavailable.
- Uses shared Python logic with thin platform adapters.
- No paid APIs or cloud services required.

Example destination:
Screenshots/2026/09 - September/29/2026-09-29_113200_Story-Studio-Error.png

Windows install:
powershell -ExecutionPolicy Bypass -File scripts/windows/install.ps1

Linux install:
bash scripts/linux/install.sh

See PLATFORM_SUPPORT.md and AGENTS.md for project rules.