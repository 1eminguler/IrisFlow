import json

from irisflow.config import GestureTimings, Settings


def test_timings_are_ordered():
    t = GestureTimings()
    assert t.reflex_blink_max < t.click_min < t.click_max
    assert t.click_max < t.settings_feedback_start < t.settings_hold < t.suspend_hold


def test_roundtrip(tmp_path):
    path = tmp_path / "settings.json"
    original = Settings(dwell_time=1.2, timings=GestureTimings(settings_hold=6.0))
    original.save(path)
    assert Settings.load(path) == original


def test_unknown_keys_are_ignored(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text(json.dumps({"dwell_time": 0.5, "old_key": 1, "timings": {"nope": 2}}))
    settings = Settings.load(path)
    assert settings.dwell_time == 0.5


def test_broken_file_falls_back_to_defaults(tmp_path):
    path = tmp_path / "settings.json"
    path.write_text("{not json")
    assert Settings.load(path) == Settings()


def test_missing_file_falls_back_to_defaults(tmp_path):
    assert Settings.load(tmp_path / "missing.json") == Settings()
