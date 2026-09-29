# Platform Support

Primary environments:
- Windows 11
- Pop!_OS 22.04 and compatible Linux

Shared behavior belongs in cross-platform Python modules.
Platform-specific path discovery and startup integration belong in thin adapters or scripts.

Startup:
- Windows: Scheduled Task
- Linux: systemd user service

OCR is local and optional. If Tesseract is unavailable, timestamp-based filenames are used.