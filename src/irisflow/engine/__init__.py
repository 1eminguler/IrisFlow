"""Gaze engine: webcam frames in, ``GazeFrame`` out.

Owner: Engine developer (see README -> Team & Ownership).

Pipeline (one pass per camera frame)::

    Camera -> IrisTracker -> HeadPoseCompensator -> BlinkDetector
                                   |
                                   v
                          CalibrationModel -> GazeFilter -> GazeFrame

Nothing in this package may import from ``irisflow.ui`` or ``irisflow.core``.
"""

from irisflow.engine.webcam_engine import WebcamGazeEngine

__all__ = ["WebcamGazeEngine"]
