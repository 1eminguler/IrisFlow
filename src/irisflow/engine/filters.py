"""Smoothing for the gaze point.

Goal: no jitter while the user fixates on a button, but no lag when they look
somewhere else.

TODO(engine):
    * Implement a One Euro Filter (good default for this exact problem).
    * Optionally add fixation detection (I-DT / I-VT) to "snap" during fixations.
"""

from __future__ import annotations

from irisflow.shared.types import Point


class GazeFilter:
    def __init__(self, min_cutoff: float = 1.0, beta: float = 0.01) -> None:
        self.min_cutoff = min_cutoff
        self.beta = beta

    def update(self, point: Point, timestamp: float) -> Point:
        raise NotImplementedError

    def reset(self) -> None:
        """Called after blinks / face loss so old data does not drag the cursor."""
        raise NotImplementedError
