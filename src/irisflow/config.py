"""User settings and gesture timings.

Shared by both sides. Defaults follow docs/gestures.md - if you change a default
here, update that document too.

Settings are stored per user (not in the repo):
    Windows: %APPDATA%/IrisFlow/settings.json
    Others:  ~/.config/irisflow/settings.json
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass, field, fields
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class GestureTimings:
    """Eye-closure durations in seconds. See docs/gestures.md."""

    reflex_blink_max: float = 0.25  # shorter closures are natural blinks -> ignored
    click_min: float = 0.5  # deliberate blink click window
    click_max: float = 1.0
    settings_feedback_start: float = 3.0  # start the "keep holding" sound
    settings_hold: float = 5.0  # release between 5 s and 10 s -> settings panel
    suspend_hold: float = 10.0  # 10 s reached -> suspend immediately
    wake_blink_count: int = 3  # deliberate blinks needed to wake up
    wake_window: float = 4.0  # ...within this many seconds


@dataclass(slots=True)
class Settings:
    camera_index: int = 0
    dwell_time: float = 0.8  # seconds of steady gaze to trigger a button
    blink_click_enabled: bool = True
    button_scale: float = 1.0  # UI size multiplier
    sound_volume: float = 0.7  # 0.0 - 1.0, feedback beeps
    tts_volume: float = 1.0  # 0.0 - 1.0, spoken output
    tts_rate: int = 160  # words per minute
    language: str = "tr"
    timings: GestureTimings = field(default_factory=GestureTimings)

    # -- persistence -------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Settings:
        """Build settings from a dict, ignoring unknown keys (old/new versions)."""
        timing_keys = {f.name for f in fields(GestureTimings)}
        timings_data = {k: v for k, v in data.get("timings", {}).items() if k in timing_keys}
        setting_keys = {f.name for f in fields(cls)} - {"timings"}
        settings_data = {k: v for k, v in data.items() if k in setting_keys}
        return cls(**settings_data, timings=GestureTimings(**timings_data))

    def save(self, path: Path | None = None) -> Path:
        path = path or default_settings_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path | None = None) -> Settings:
        """Load settings, falling back to defaults if the file is missing or broken."""
        path = path or default_settings_path()
        try:
            return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError, TypeError):
            return cls()


def default_settings_path() -> Path:
    if sys.platform == "win32" and os.environ.get("APPDATA"):
        return Path(os.environ["APPDATA"]) / "IrisFlow" / "settings.json"
    return Path.home() / ".config" / "irisflow" / "settings.json"
