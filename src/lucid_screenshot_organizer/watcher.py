from __future__ import annotations

import logging
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .config import Settings
from .organizer import organize_file

log = logging.getLogger(__name__)


class ScreenshotHandler(FileSystemEventHandler):
    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings

    def on_created(self, event) -> None:
        if event.is_directory:
            return
        try:
            organize_file(Path(event.src_path), self.settings)
        except Exception:
            log.exception("Failed to process screenshot: %s", event.src_path)

    def on_moved(self, event) -> None:
        if event.is_directory:
            return
        try:
            organize_file(Path(event.dest_path), self.settings)
        except Exception:
            log.exception("Failed to process moved screenshot: %s", event.dest_path)


def run_watcher(settings: Settings) -> None:
    settings.source_dir.mkdir(parents=True, exist_ok=True)
    settings.destination_root.mkdir(parents=True, exist_ok=True)
    observer = Observer()
    observer.schedule(ScreenshotHandler(settings), str(settings.source_dir), recursive=settings.recursive)
    observer.start()
    log.info("Watching %s", settings.source_dir)
    log.info("Destination %s", settings.destination_root)
    try:
        observer.join()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()