"""Smoke test: every non-UI module must import without a camera or display."""

import importlib

import pytest

MODULES = [
    "irisflow",
    "irisflow.config",
    "irisflow.app",
    "irisflow.shared",
    "irisflow.shared.mock_engine",
    "irisflow.engine",
    "irisflow.engine.camera",
    "irisflow.engine.iris_tracker",
    "irisflow.engine.head_pose",
    "irisflow.engine.blink",
    "irisflow.engine.calibration",
    "irisflow.engine.filters",
    "irisflow.core.state_machine",
    "irisflow.core.dwell",
    "irisflow.services.tts",
    "irisflow.services.sounds",
    "irisflow.services.cursor",
    "irisflow.predict.predictor",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)
