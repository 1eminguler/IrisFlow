"""Head-pose compensation.

The user's head is *supposed* to be still, but even a 1 cm shift ruins a naive
iris -> screen mapping. This module turns raw landmarks into an eye feature that
is (mostly) independent of small head movements.

TODO(engine):
    * Normalize the iris center relative to the eye corners (eye-local coordinates).
    * Estimate head yaw/pitch (e.g. ``cv2.solvePnP`` on a few stable face points)
      and correct the feature for it.
    * Output a ``Point`` that goes into ``GazeFrame.eye_feature``.
"""

from __future__ import annotations

from irisflow.engine.iris_tracker import FaceLandmarks
from irisflow.shared.types import Point


class HeadPoseCompensator:
    def eye_feature(self, face: FaceLandmarks) -> Point:
        raise NotImplementedError
