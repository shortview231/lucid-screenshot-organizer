from datetime import datetime
from pathlib import Path

from lucid_screenshot_organizer.naming import build_filename, make_label, unique_path


def test_make_label_uses_useful_words():
    label = make_label("Story Studio timeline error while loading event inspector")
    assert label.startswith("Story-Studio-timeline-error")


def test_build_filename_falls_back_to_screenshot():
    name = build_filename(Path("Screenshot.png"), "", datetime(2026, 9, 29, 11, 30, 5))
    assert name == "2026-09-29_113005_Screenshot.png"


def test_unique_path_adds_counter(tmp_path):
    path = tmp_path / "shot.png"
    path.write_text("a")
    assert unique_path(path).name == "shot_2.png"