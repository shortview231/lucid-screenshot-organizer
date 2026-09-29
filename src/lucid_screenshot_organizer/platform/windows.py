from __future__ import annotations

import os
from pathlib import Path


def _pictures_dir() -> Path:
    onedrive = os.environ.get("OneDrive")
    if onedrive:
        candidate = Path(onedrive) / "Pictures"
        if candidate.exists():
            return candidate
    return Path.home() / "Pictures"


def get_default_screenshot_dir() -> Path:
    return _pictures_dir() / "Screenshots"


def get_default_destination_root() -> Path:
    return _pictures_dir() / "Lucid Screenshots"