"""A fake gaze engine for developing the app without a camera.

Controls (default input sources):
    * Mouse position  -> gaze point
    * Hold Space      -> eyes closed

Run with: ``python -m irisflow --mock``

The input sources are injectable so tests can drive the engine without a real
mouse or keyboard.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable, Sequence

from irisflow.shared.types import CalibrationResult, CalibrationSample, GazeFrame, Point

PointerFn = Callable[[], tuple[float, float]]
ClosedFn = Callable[[], bool]


class MockGazeEngine:
    """Implements ``irisflow.shared.GazeEngine`` using mouse and keyboard."""

    def __init__(
        self,
        screen_size: tuple[int, int] = (1920, 1080),
        pointer_fn: PointerFn | None = None,
        closed_fn: ClosedFn | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._screen_w, self._screen_h = screen_size
        self._pointer_fn = pointer_fn
        self._closed_fn = closed_fn
        self._clock = clock
        self._running = False
        self._calibrated = True  # the mouse is already in screen coordinates
        self._low_power = False

        # Only used by the default pynput sources.
        self._space_down = threading.Event()
        self._listener = None

    # -- GazeEngine protocol ---------------------------------------------------

    def start(self) -> None:
        if self._running:
            return
        if self._pointer_fn is None or self._closed_fn is None:
            self._setup_default_sources()
        self._running = True

    def stop(self) -> None:
        self._running = False
        if self._listener is not None:
            self._listener.stop()
            self._listener = None

    def read(self) -> GazeFrame | None:
        if not self._running:
            return None
        assert self._pointer_fn is not None and self._closed_fn is not None

        x, y = self._pointer_fn()
        closed = self._closed_fn()
        gaze = Point(float(x), float(y))
        feature = Point(gaze.x / self._screen_w, gaze.y / self._screen_h)
        return GazeFrame(
            timestamp=self._clock(),
            face_found=True,
            eyes_closed=closed,
            gaze=None if closed or not self._calibrated else gaze,
            eye_feature=None if closed else feature,
            confidence=1.0,
        )

    def calibrate(self, samples: Sequence[CalibrationSample]) -> CalibrationResult:
        if not samples:
            return CalibrationResult(success=False, message="No samples collected.")
        self._calibrated = True
        return CalibrationResult(success=True, mean_error_px=0.0, message="Mock calibration.")

    def set_low_power(self, enabled: bool) -> None:
        self._low_power = enabled

    # -- helpers -----------------------------------------------------------------

    @property
    def low_power(self) -> bool:
        return self._low_power

    def _setup_default_sources(self) -> None:
        # Imported lazily so tests and CI never need a display or input devices.
        from pynput import keyboard, mouse

        mouse_ctl = mouse.Controller()

        def on_press(key: object) -> None:
            if key == keyboard.Key.space:
                self._space_down.set()

        def on_release(key: object) -> None:
            if key == keyboard.Key.space:
                self._space_down.clear()

        self._listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._listener.daemon = True
        self._listener.start()

        if self._pointer_fn is None:
            self._pointer_fn = lambda: mouse_ctl.position
        if self._closed_fn is None:
            self._closed_fn = self._space_down.is_set
