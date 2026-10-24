from irisflow.shared.types import GazeFrame, Point


def test_usable_frame():
    frame = GazeFrame(timestamp=1.0, face_found=True, eyes_closed=False, gaze=Point(10, 20))
    assert frame.is_usable


def test_closed_eyes_frame_is_not_usable():
    frame = GazeFrame(timestamp=1.0, face_found=True, eyes_closed=True, gaze=Point(10, 20))
    assert not frame.is_usable


def test_frame_without_gaze_is_not_usable():
    frame = GazeFrame(timestamp=1.0, face_found=True, eyes_closed=False)
    assert not frame.is_usable
