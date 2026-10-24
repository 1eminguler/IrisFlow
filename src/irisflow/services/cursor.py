"""Control of the real OS mouse cursor (for using other apps, not just IrisFlow).

TODO(app):
    * Move the cursor to the gaze point (pynput ``mouse.Controller``).
    * Left click on dwell / blink click.
    * Must be easy to disable - while the mock engine reads the mouse, moving
      it as well creates a feedback loop.
"""

from __future__ import annotations

from irisflow.shared.types import Point


class SystemCursor:
    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def move_to(self, point: Point) -> None:
        raise NotImplementedError

    def click(self) -> None:
        raise NotImplementedError
