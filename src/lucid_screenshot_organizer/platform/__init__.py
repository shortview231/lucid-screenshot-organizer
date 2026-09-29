from __future__ import annotations

import os

if os.name == "nt":
    from .windows import get_default_destination_root, get_default_screenshot_dir
else:
    from .linux import get_default_destination_root, get_default_screenshot_dir

__all__ = ["get_default_destination_root", "get_default_screenshot_dir"]