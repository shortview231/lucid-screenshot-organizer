from __future__ import annotations

import logging
import os
from pathlib import Path

from .config import load_settings
from .watcher import run_watcher


def _log_dir() -> Path:
    override = os.environ.get("LUCID_SCREENSHOT_LOG_DIR")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    else:
        base = Path(os.environ.get("XDG_STATE_HOME", str(Path.home() / ".local" / "state")))
    return base / "lucid-screenshot-organizer"


def main() -> None:
    settings = load_settings()
    log_dir = _log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "organizer.log"
    logging.basicConfig(
        level=getattr(logging, settings.log_level, logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
    )
    run_watcher(settings)


if __name__ == "__main__":
    main()