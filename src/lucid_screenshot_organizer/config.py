from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from .platform import get_default_destination_root, get_default_screenshot_dir


@dataclass(frozen=True)
class Settings:
    source_dir: Path
    destination_root: Path
    recursive: bool = False
    minimum_ocr_characters: int = 4
    max_label_words: int = 6
    settle_seconds: float = 1.0
    log_level: str = "INFO"


def default_config_path() -> Path:
    override = os.environ.get("LUCID_SCREENSHOT_CONFIG")
    if override:
        return Path(override).expanduser()
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home())))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    return base / "lucid-screenshot-organizer" / "config.toml"


def load_settings(path: Path | None = None) -> Settings:
    path = path or default_config_path()
    raw: dict = {}
    if path.exists():
        with path.open("rb") as fh:
            raw = tomllib.load(fh)

    source_raw = raw.get("source", {}).get("directory", "")
    dest_raw = raw.get("destination", {}).get("root", "")
    organizer = raw.get("organizer", {})
    logging = raw.get("logging", {})

    source = Path(source_raw).expanduser() if source_raw else get_default_screenshot_dir()
    destination = Path(dest_raw).expanduser() if dest_raw else get_default_destination_root()

    return Settings(
        source_dir=source,
        destination_root=destination,
        recursive=bool(organizer.get("recursive", False)),
        minimum_ocr_characters=int(organizer.get("minimum_ocr_characters", 4)),
        max_label_words=int(organizer.get("max_label_words", 6)),
        settle_seconds=float(organizer.get("settle_seconds", 1.0)),
        log_level=str(logging.get("level", "INFO")).upper(),
    )