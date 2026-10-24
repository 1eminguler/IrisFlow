"""Face / eye / iris landmark extraction.

TODO(engine):
    * Use MediaPipe Face Landmarker (Tasks API) with the model file in ``models/``
      (see models/README.md). It returns 478 landmarks including the irises.
    * Extract per eye: iris center, eye corners, upper/lower lid points.
    * Return ``None`` when no face is found.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from irisflow.shared.types import Point


@dataclass(frozen=True, slots=True)
class EyeLandmarks:
    iris_center: Point  # pixels in the camera image
    inner_corner: Point
    outer_corner: Point
    lid_points: tuple[Point, ...]  # used for the eye aspect ratio (EAR)


@dataclass(frozen=True, slots=True)
class FaceLandmarks:
    left_eye: EyeLandmarks
    right_eye: EyeLandmarks
    all_points: np.ndarray  # (478, 3) raw landmarks, needed for head pose


class IrisTracker:
    def __init__(self, model_path: str = "models/face_landmarker.task") -> None:
        self.model_path = model_path

    def process(self, image_bgr: np.ndarray, timestamp: float) -> FaceLandmarks | None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError
