from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

_STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "from", "your", "you",
    "are", "was", "have", "has", "not", "but", "into", "http", "https",
}


def _clean_token(token: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "", token)


def make_label(text: str, max_words: int = 6) -> str:
    words: list[str] = []
    for raw in re.findall(r"[A-Za-z0-9][A-Za-z0-9._-]*", text):
        token = _clean_token(raw)
        if len(token) < 3 or token.lower() in _STOPWORDS:
            continue
        words.append(token)
        if len(words) >= max_words:
            break
    return "-".join(words)


def build_filename(original: Path, text: str, taken_at: datetime, max_words: int = 6) -> str:
    stamp = taken_at.strftime("%Y-%m-%d_%H%M%S")
    label = make_label(text, max_words=max_words)
    suffix = original.suffix.lower() or ".png"
    if label:
        return f"{stamp}_{label}{suffix}"
    return f"{stamp}_Screenshot{suffix}"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(2, 10000):
        candidate = path.with_name(f"{path.stem}_{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Unable to create unique destination for {path}")