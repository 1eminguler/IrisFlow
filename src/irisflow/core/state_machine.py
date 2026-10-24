"""Eye-closure timing state machine (meta-gestures).

Turns the per-frame ``eyes_closed`` flag into actions. The full spec with
all time ranges is in docs/gestures.md.

TODO(app):
    * Track when the eyes closed / opened (use ``GazeFrame.timestamp``, never
      wall-clock time, so tests can feed fake timestamps).
    * Decide CLICK / OPEN_SETTINGS on *release*, SUSPEND as soon as the hold
      reaches ``suspend_hold``.
    * Emit FEEDBACK_* actions so the UI can play the progress sounds.
    * In SUSPENDED mode only listen for the wake-up gesture.
    * Treat ``face_found == False`` as "unknown", NOT as "eyes closed".
"""

from __future__ import annotations

from enum import Enum, auto

from irisflow.config import GestureTimings
from irisflow.shared.types import GazeFrame


class Mode(Enum):
    ACTIVE = auto()  # normal use: gaze moves focus, dwell/blink clicks
    SETTINGS = auto()  # settings & calibration panel is open
    SUSPENDED = auto()  # tracking paused, only the wake-up gesture works


class Action(Enum):
    NONE = auto()
    CLICK = auto()
    FEEDBACK_HOLD_STARTED = auto()  # passed settings_feedback_start (3 s)
    FEEDBACK_SETTINGS_ARMED = auto()  # passed settings_hold (5 s)
    OPEN_SETTINGS = auto()
    SUSPEND = auto()
    WAKE = auto()


class GestureStateMachine:
    def __init__(self, timings: GestureTimings | None = None) -> None:
        self.timings = timings or GestureTimings()
        self.mode = Mode.ACTIVE

    def update(self, frame: GazeFrame) -> Action:
        """Feed one frame, get back the action it triggers (usually NONE)."""
        raise NotImplementedError

    def reset(self) -> None:
        raise NotImplementedError
