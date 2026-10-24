"""Emergency / basic need cards - big buttons that speak out loud.

TODO(app): grid of large cards, dwell or blink to trigger, speak ``speech``
through ``services.tts.Speaker`` and show a visible confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtWidgets import QWidget


@dataclass(frozen=True, slots=True)
class NeedCard:
    id: str
    label: str  # shown on the button
    speech: str  # spoken out loud


NEED_CARDS: tuple[NeedCard, ...] = (
    NeedCard("water", "Su", "Su istiyorum."),
    NeedCard("pain", "Ağrı / İlaç", "Ağrım var, ilacıma ihtiyacım var."),
    NeedCard("position", "Pozisyon Değiştir", "Pozisyonumu değiştirir misiniz?"),
    NeedCard("caregiver", "Refakatçi Çağır", "Lütfen yanıma gelir misiniz?"),
)


class NeedCardsScreen(QWidget):
    pass
