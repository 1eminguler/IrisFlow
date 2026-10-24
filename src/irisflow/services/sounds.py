"""Short feedback sounds (hold progress, click, suspend, wake).

TODO(app): play short beeps without blocking (e.g. ``QSoundEffect`` with wav
files in ``assets/sounds/``).
"""

from __future__ import annotations

from enum import Enum, auto


class Sound(Enum):
    CLICK = auto()
    HOLD_STARTED = auto()
    SETTINGS_ARMED = auto()
    SUSPENDED = auto()
    WOKE_UP = auto()


class FeedbackSounds:
    def __init__(self, volume: float = 0.7) -> None:
        self.volume = volume

    def play(self, sound: Sound) -> None:
        raise NotImplementedError
