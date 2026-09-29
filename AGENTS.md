# Agent Instructions

This project supports Windows 11 and Pop!_OS Linux.

- Keep shared logic platform-independent.
- Isolate OS-specific behavior under src/lucid_screenshot_organizer/platform and scripts/<os>.
- Do not hard-code user-specific paths in shared code.
- Do not add paid APIs, metered cloud services, or required cloud dependencies.
- Never delete screenshots during normal processing.
- Never overwrite an existing destination file.
- Any feature touching paths, startup, shell commands, services, notifications, or filesystem behavior must account for both supported platforms.