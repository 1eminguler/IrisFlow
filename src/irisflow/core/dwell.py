"""Dwell-time clicking: look at a target long enough and it fires.

TODO(app):
    * Track which target (button id) the gaze is currently inside.
    * Expose progress 0.0-1.0 for the circular countdown ring.
    * Fire once per dwell; the user must look away (or wait a cooldown)
      before the same target can fire again.
    * Small tolerance: a few frames outside the target should not reset progress.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DwellState:
    target_id: str | None
    progress: float  # 0.0 - 1.0
    fired: bool  # True only on the frame the dwell completes


class DwellTracker:
    def __init__(self, dwell_time: float = 0.8) -> None:
        self.dwell_time = dwell_time

    def update(self, target_id: str | None, timestamp: float) -> DwellState:
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
