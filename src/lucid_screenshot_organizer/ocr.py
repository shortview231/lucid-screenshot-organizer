from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

log = logging.getLogger(__name__)


def extract_text(path: Path) -> str:
    try:
        import pytesseract
        with Image.open(path) as image:
            return pytesseract.image_to_string(image).strip()
    except Exception as exc:
        log.debug("OCR unavailable or failed for %s: %s", path, exc)
        return ""