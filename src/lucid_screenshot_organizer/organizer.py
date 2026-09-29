from __future__ import annotations

import logging
import shutil
import time
from datetime import datetime
from pathlib import Path

from PIL import Image

from .config import Settings
from .naming import build_filename, unique_path
from .ocr import extract_text

log = logging.getLogger(__name__)
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _wait_until_stable(path: Path, settle_seconds: float) -> bool:
    previous = -1
    stable_count = 0
    deadline = time.monotonic() + max(10.0, settle_seconds * 10)
    while time.monotonic() < deadline:
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        if size > 0 and size == previous:
            stable_count += 1
            if stable_count >= 2:
                return True
        else:
            stable_count = 0
        previous = size
        time.sleep(settle_seconds)
    return False


def _image_is_readable(path: Path) -> bool:
    try:
        with Image.open(path) as image:
            image.verify()
        return True
    except Exception:
        return False


def organize_file(path: Path, settings: Settings) -> Path | None:
    path = Path(path)
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS or not path.is_file():
        return None
    if settings.destination_root in path.parents:
        return None
    if not _wait_until_stable(path, settings.settle_seconds):
        log.warning("File never stabilized: %s", path)
        return None
    if not _image_is_readable(path):
        log.warning("Not a readable image: %s", path)
        return None

    taken_at = datetime.fromtimestamp(path.stat().st_mtime)
    text = extract_text(path)
    if len(text.strip()) < settings.minimum_ocr_characters:
        text = ""

    destination_dir = (
        settings.destination_root
        / taken_at.strftime("%Y")
        / taken_at.strftime("%m - %B")
        / taken_at.strftime("%d")
    )
    destination_dir.mkdir(parents=True, exist_ok=True)
    filename = build_filename(path, text, taken_at, settings.max_label_words)
    destination = unique_path(destination_dir / filename)
    shutil.move(str(path), str(destination))
    log.info("Moved %s -> %s", path, destination)
    return destination