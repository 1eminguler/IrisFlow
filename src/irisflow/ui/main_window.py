"""Main window.

Right now this is only a development harness: it polls the engine, draws the
gaze point and shows the raw eye state. It proves the engine -> app pipeline
works end to end. Replace the drawing with the real UI.

TODO(app):
    * Feed every frame into GestureStateMachine and DwellTracker.
    * Host the screens: need cards, keyboard, settings, calibration, suspended.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QKeyEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import QWidget

from irisflow.config import Settings
from irisflow.shared.interfaces import GazeEngine
from irisflow.shared.types import GazeFrame

POLL_INTERVAL_MS = 33  # ~30 Hz


class MainWindow(QWidget):
    def __init__(self, engine: GazeEngine, settings: Settings) -> None:
        super().__init__()
        self.engine = engine
        self.settings = settings
        self.last_frame: GazeFrame | None = None

        self.setWindowTitle("IrisFlow")
        self.setMinimumSize(800, 600)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._poll_engine)
        self._timer.start(POLL_INTERVAL_MS)

    def _poll_engine(self) -> None:
        self.last_frame = self.engine.read()
        self.update()

    # -- dev harness drawing -------------------------------------------------------

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802 (Qt naming)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#101418"))

        frame = self.last_frame
        painter.setPen(QColor("#e6e6e6"))
        painter.setFont(QFont("Segoe UI", 14))
        painter.drawText(20, 36, self._status_text(frame))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(20, 60, "Esc: quit")

        if frame is not None and frame.gaze is not None:
            local = self.mapFromGlobal(QPoint(int(frame.gaze.x), int(frame.gaze.y)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(80, 200, 255, 160))
            painter.drawEllipse(local, 28, 28)

    @staticmethod
    def _status_text(frame: GazeFrame | None) -> str:
        if frame is None:
            return "Waiting for engine..."
        if not frame.face_found:
            return "No face"
        eyes = "CLOSED" if frame.eyes_closed else "open"
        return f"Eyes: {eyes}   confidence: {frame.confidence:.2f}"

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802 (Qt naming)
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)
