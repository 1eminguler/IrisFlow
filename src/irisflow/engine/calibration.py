"""Eye feature -> screen coordinate mapping.

TODO(engine):
    * Fit a 2nd-order polynomial regression (or homography) from the collected
      ``CalibrationSample`` list. 5 targets (4 corners + center) is the minimum;
      consider 9 for better accuracy.
    * Drop outlier samples (saccades, half-blinks) before fitting.
    * Report the mean error in pixels so the UI can ask the user to recalibrate.
    * Save / load the fitted model so the user does not recalibrate on every start.
"""

from __future__ import annotations

from collections.abc import Sequence

from irisflow.shared.types import CalibrationResult, CalibrationSample, Point


class CalibrationModel:
    @property
    def is_fitted(self) -> bool:
        raise NotImplementedError

    def fit(self, samples: Sequence[CalibrationSample]) -> CalibrationResult:
        raise NotImplementedError

    def predict(self, eye_feature: Point) -> Point:
        """Map an eye feature to a screen position in pixels."""
        raise NotImplementedError

    def save(self, path: str) -> None:
        raise NotImplementedError

    def load(self, path: str) -> None:
        raise NotImplementedError
