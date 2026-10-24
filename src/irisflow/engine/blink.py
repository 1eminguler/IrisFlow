"""Eye open/closed detection.

Only reports the RAW state per frame. Durations (reflex blink vs. click vs.
settings vs. suspend) are measured in ``irisflow.core.state_machine``.

TODO(engine):
    * Compute the Eye Aspect Ratio (EAR) for both eyes.
    * Closed = both eyes below threshold. Use hysteresis (separate close/open
      thresholds) so the state does not flicker around the threshold.
    * Make the threshold adjustable (it differs per person) - ideally measured
      during calibration.
"""

from __future__ import annotations

from irisflow.engine.iris_tracker import FaceLandmarks


class BlinkDetector:
    def __init__(self, close_threshold: float = 0.20, open_threshold: float = 0.25) -> None:
        self.close_threshold = close_threshold
        self.open_threshold = open_threshold

    def update(self, face: FaceLandmarks) -> bool:
        """Return True if the eyes are considered closed in this frame."""
        raise NotImplementedError
