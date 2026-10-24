"""Shared contract between the gaze engine and the application.

Everything in this package is used by BOTH sides of the project.
Changes here must be agreed on by both developers (see CONTRIBUTING.md).
"""

from irisflow.shared.interfaces import GazeEngine
from irisflow.shared.types import CalibrationResult, CalibrationSample, GazeFrame, Point

__all__ = [
    "CalibrationResult",
    "CalibrationSample",
    "GazeEngine",
    "GazeFrame",
    "Point",
]
