"""Virtual keyboard with word prediction.

TODO(app):
    * Large keys, Turkish layout (ç ğ ı ö ş ü), space, delete, speak, clear.
    * Suggestion row fed by ``irisflow.predict.predictor.WordPredictor``.
    * Consider a grouped layout (pick a group, then a letter) to keep keys big.
"""

from __future__ import annotations

from PySide6.QtWidgets import QWidget


class VirtualKeyboard(QWidget):
    pass
