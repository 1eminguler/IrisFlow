"""Webcam capture.

TODO(engine):
    * Open the camera with OpenCV (``cv2.VideoCapture``; on Windows try ``cv2.CAP_DSHOW``).
    * Capture on a background thread and keep only the latest frame (no queue
      build-up -> no lag).
    * Attach a ``time.monotonic()`` timestamp to every frame.
    * Support changing FPS at runtime (low-power mode).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class CameraFrame:
    image: np.ndarray  # BGR, as returned by OpenCV
    timestamp: float


class Camera:
    def __init__(self, index: int = 0, width: int = 1280, height: int = 720, fps: int = 30) -> None:
        self.index = index
        self.width = width
        self.height = height
        self.fps = fps

    def open(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

    def latest(self) -> CameraFrame | None:
        """Most recent frame, or None if nothing has been captured yet."""
        raise NotImplementedError

    def set_fps(self, fps: int) -> None:
        raise NotImplementedError
