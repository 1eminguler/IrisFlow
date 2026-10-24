"""Calibration screen.

TODO(app):
    * Full screen, show each target in ``TARGETS`` one by one (with a short
      "settle" delay before collecting, the eye needs ~300 ms to land).
    * Collect ``CalibrationSample(target, frame.eye_feature)`` from every usable
      frame while the target is shown.
    * Call ``engine.calibrate(samples)`` and show the result; offer a retry if
      ``mean_error_px`` is too high.
"""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

# Normalized (0-1) screen positions: 4 corners (with margin) + center.
TARGETS: tuple[tuple[float, float], ...] = (
    (0.5, 0.5),
    (0.1, 0.1),
    (0.9, 0.1),
    (0.9, 0.9),
    (0.1, 0.9),
)


class CalibrationScreen(QWidget):
    pass
