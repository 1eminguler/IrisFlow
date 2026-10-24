"""Application wiring: pick an engine, load settings, open the window."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from irisflow import __version__
from irisflow.config import Settings
from irisflow.shared.interfaces import GazeEngine


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="irisflow", description="Eye-controlled computer access.")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="use the mock engine (mouse = gaze, hold Space = eyes closed)",
    )
    parser.add_argument("--camera", type=int, default=None, help="camera index (default: settings)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args(argv)


def create_engine(
    args: argparse.Namespace, settings: Settings, screen_size: tuple[int, int]
) -> GazeEngine:
    if args.mock:
        from irisflow.shared.mock_engine import MockGazeEngine

        return MockGazeEngine(screen_size=screen_size)

    from irisflow.engine import WebcamGazeEngine

    camera = args.camera if args.camera is not None else settings.camera_index
    return WebcamGazeEngine(camera_index=camera)


def run(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    settings = Settings.load()

    from PySide6.QtWidgets import QApplication

    from irisflow.ui.main_window import MainWindow

    app = QApplication(sys.argv[:1])
    geometry = app.primaryScreen().geometry()
    engine = create_engine(args, settings, (geometry.width(), geometry.height()))

    try:
        engine.start()
    except NotImplementedError as exc:
        print(f"[irisflow] {exc}", file=sys.stderr)
        return 1

    window = MainWindow(engine, settings)
    window.showMaximized()
    try:
        return app.exec()
    finally:
        engine.stop()
