"""Text-to-speech for need cards and typed text.

TODO(app):
    * Use pyttsx3 (offline, works with Windows SAPI voices).
    * Pick a Turkish voice if one is installed, otherwise fall back to default.
    * Speak without freezing the UI (separate thread / queue).
"""

from __future__ import annotations


class Speaker:
    def __init__(self, volume: float = 1.0, rate: int = 160, language: str = "tr") -> None:
        self.volume = volume
        self.rate = rate
        self.language = language

    def say(self, text: str) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError
