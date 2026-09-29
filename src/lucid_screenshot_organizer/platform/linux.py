from __future__ import annotations

from pathlib import Path


def _pictures_dir() -> Path:
    user_dirs = Path.home() / ".config" / "user-dirs.dirs"
    if user_dirs.exists():
        for line in user_dirs.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("XDG_PICTURES_DIR="):
                value = line.split("=", 1)[1].strip().strip('"').replace("$HOME", str(Path.home()))
                return Path(value)
    return Path.home() / "Pictures"


def get_default_screenshot_dir() -> Path:
    pictures = _pictures_dir()
    for name in ("Screenshots", "screenshots"):
        candidate = pictures / name
        if candidate.exists():
            return candidate
    return pictures / "Screenshots"


def get_default_destination_root() -> Path:
    return _pictures_dir() / "Lucid Screenshots"