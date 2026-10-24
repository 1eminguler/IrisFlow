"""The real gaze engine. Wires the engine modules together.

TODO(engine): implement every method by combining Camera, IrisTracker,
HeadPoseCompensator, BlinkDetector, CalibrationModel and GazeFilter.
Run the pipeline on a background thread and store the latest ``GazeFrame``.
"""

from __future__ import annotations

from collections.abc import Sequence

from irisflow.shared.types import CalibrationResult, CalibrationSample, GazeFrame


class WebcamGazeEngine:
    """Implements ``irisflow.shared.GazeEngine``."""

    def __init__(self, camera_index: int = 0) -> None:
        self.camera_index = camera_index

    def start(self) -> None:
        raise NotImplementedError("Real engine is not implemented yet. Use --mock.")

    def stop(self) -> None:
        pass

    def read(self) -> GazeFrame | None:
        raise NotImplementedError

    def calibrate(self, samples: Sequence[CalibrationSample]) -> CalibrationResult:
        raise NotImplementedError

    def set_low_power(self, enabled: bool) -> None:
        raise NotImplementedError
