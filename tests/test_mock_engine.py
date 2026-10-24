from irisflow.shared import GazeEngine
from irisflow.shared.mock_engine import MockGazeEngine
from irisflow.shared.types import CalibrationSample, Point


def make_engine(pointer=(960, 540), closed=False):
    state = {"pointer": pointer, "closed": closed, "t": 0.0}
    engine = MockGazeEngine(
        screen_size=(1920, 1080),
        pointer_fn=lambda: state["pointer"],
        closed_fn=lambda: state["closed"],
        clock=lambda: state["t"],
    )
    return engine, state


def test_follows_the_protocol():
    engine, _ = make_engine()
    assert isinstance(engine, GazeEngine)


def test_returns_none_before_start():
    engine, _ = make_engine()
    assert engine.read() is None


def test_pointer_becomes_gaze():
    engine, state = make_engine(pointer=(100, 200))
    engine.start()
    state["t"] = 5.0
    frame = engine.read()
    assert frame is not None
    assert frame.gaze == Point(100, 200)
    assert frame.timestamp == 5.0
    assert frame.eye_feature == Point(100 / 1920, 200 / 1080)
    assert not frame.eyes_closed


def test_closed_eyes_have_no_gaze():
    engine, state = make_engine()
    engine.start()
    state["closed"] = True
    frame = engine.read()
    assert frame is not None
    assert frame.eyes_closed
    assert frame.gaze is None


def test_calibrate_needs_samples():
    engine, _ = make_engine()
    assert not engine.calibrate([]).success
    sample = CalibrationSample(target=Point(0, 0), eye_feature=Point(0, 0))
    assert engine.calibrate([sample]).success


def test_low_power_flag():
    engine, _ = make_engine()
    engine.set_low_power(True)
    assert engine.low_power
