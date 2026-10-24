"""Data types that flow from the engine to the application.

The engine produces one ``GazeFrame`` per processed camera frame. The application
never touches the camera or MediaPipe directly - it only consumes these frames.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple


class Point(NamedTuple):
    """A 2D point. Unit depends on context (screen pixels or normalized 0-1)."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class GazeFrame:
    """Snapshot of the user's eye state at a single moment.

    Attributes:
        timestamp: ``time.monotonic()`` seconds when the camera frame was captured.
        face_found: False when no face is visible (user left, bad lighting, etc.).
        eyes_closed: True while BOTH eyes are closed. The engine only reports the
            raw state; measuring how long the eyes stay closed is the job of
            ``irisflow.core.state_machine``.
        gaze: Smoothed gaze position in screen pixels. ``None`` if the system is
            not calibrated yet or no face is found.
        eye_feature: Raw, unfiltered, head-pose-compensated iris position in a
            normalized eye space. Used only to collect calibration samples.
        confidence: 0.0-1.0, how much the engine trusts this frame.
    """

    timestamp: float
    face_found: bool
    eyes_closed: bool
    gaze: Point | None = None
    eye_feature: Point | None = None
    confidence: float = 0.0

    @property
    def is_usable(self) -> bool:
        """True if the frame carries a gaze point the app can act on."""
        return self.face_found and not self.eyes_closed and self.gaze is not None


@dataclass(frozen=True, slots=True)
class CalibrationSample:
    """One measurement taken while the user looks at a known target.

    The calibration screen collects many samples per target point and passes
    all of them to ``GazeEngine.calibrate``.
    """

    target: Point  # where the dot was drawn, in screen pixels
    eye_feature: Point  # GazeFrame.eye_feature at that moment


@dataclass(frozen=True, slots=True)
class CalibrationResult:
    """Outcome of a calibration attempt."""

    success: bool
    mean_error_px: float | None = None  # average error on the calibration points
    message: str = ""
