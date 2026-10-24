"""The single interface the application uses to talk to a gaze engine.

There are two implementations:

* ``irisflow.engine.WebcamGazeEngine`` - the real one (webcam + MediaPipe).
* ``irisflow.shared.mock_engine.MockGazeEngine`` - mouse = gaze, Space = eyes
  closed. Lets the UI be developed and tested without a camera.

The app must only depend on this protocol, never on a concrete engine.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from irisflow.shared.types import CalibrationResult, CalibrationSample, GazeFrame


@runtime_checkable
class GazeEngine(Protocol):
    def start(self) -> None:
        """Open the camera / input source and begin producing frames."""
        ...

    def stop(self) -> None:
        """Release the camera and any background threads. Safe to call twice."""
        ...

    def read(self) -> GazeFrame | None:
        """Return the most recent frame without blocking.

        Returns ``None`` if no frame has been produced yet. The app polls this
        from a UI timer (~30 Hz); the engine is free to run its own thread.
        """
        ...

    def calibrate(self, samples: Sequence[CalibrationSample]) -> CalibrationResult:
        """Fit the eye-feature -> screen mapping from the collected samples."""
        ...

    def set_low_power(self, enabled: bool) -> None:
        """Switch to a lower frame rate while the app is suspended.

        Even in low-power mode the engine must keep reporting ``eyes_closed``
        so the wake-up gesture can be detected.
        """
        ...
