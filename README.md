# IrisFlow

[![CI](https://github.com/1eminguler/IrisFlow/actions/workflows/ci.yml/badge.svg)](https://github.com/1eminguler/IrisFlow/actions/workflows/ci.yml)

IrisFlow is an accessibility software that enables individuals with severe physical impairments of
the hands and arms (such as ALS, advanced spinal cord injury, muscular dystrophy, etc.) to
independently control a standard computer and a custom communication interface solely through
iris movements, requiring no external hardware or head motion.

It runs on an ordinary laptop webcam instead of expensive infrared eye trackers.

> **Status:** early development. The project skeleton, shared contract and a mock engine are in
> place; the real tracking engine and the UI are being built.

---

## Table of contents

- [Why](#why)
- [Features](#features)
- [How it works](#how-it-works)
- [Eye gestures](#eye-gestures)
- [Getting started](#getting-started)
- [Project structure](#project-structure)
- [Team & ownership](#team--ownership)
- [Roadmap](#roadmap)
- [Known limitations](#known-limitations)
- [Privacy](#privacy)
- [Disclaimer](#disclaimer)

## Why

| Problem | IrisFlow's answer |
|---------|-------------------|
| Head-tracking mice tire the neck and are unusable for people who cannot move their head | Only the eyes move, the head stays still |
| Medical-grade eye trackers cost thousands of dollars | Works with the webcam the user already has |
| Pausing or configuring existing tools needs a caregiver to touch the keyboard | Every system function, including settings and pause, is reachable with the eyes |
| Natural blinks and eye jitter cause accidental clicks | Reflex blinks are ignored and the gaze point is filtered |

## Features

- **5-second calibration** - look at 5 dots (4 corners + center).
- **Gaze focus** - the highlighted item follows where you look, without jitter.
- **Dwell click** - look at a button for ~0.8 s; a ring fills up and the button fires.
- **Blink click** - optional alternative: close the eyes for 0.5 - 1 s.
- **Eye-only system control** - hold the eyes closed to open settings or pause tracking.
- **Need cards** - big buttons (Water, Pain / Medicine, Change Position, Call Caregiver) that
  speak out loud.
- **Virtual keyboard with word prediction** - type with as few glances as possible.

## How it works

```
Webcam ─> Face & iris landmarks ─> Head-pose compensation ─> Calibration mapping ─> Smoothing
                    │                                                                  │
                    └──> Eye open/closed (EAR) ─────────────────────────────────┐      │
                                                                                ▼      ▼
                                                                             GazeFrame
                                                                                │
                                   Gesture state machine + dwell tracker <──────┘
                                                   │
                                     UI · Text-to-speech · OS cursor
```

The **engine** turns camera frames into `GazeFrame` objects (where the user looks, whether the
eyes are closed). The **app** consumes those frames and does everything else. The two halves only
share the small contract in `src/irisflow/shared/`, so they can be developed in parallel.

More detail: [docs/architecture.md](docs/architecture.md)

**Tech stack:** Python 3.11 · OpenCV · MediaPipe Face Landmarker · NumPy · PySide6 (Qt) ·
pyttsx3 · pynput

## Eye gestures

| Eyes closed for | Result |
|-----------------|--------|
| < 0.25 s | Natural blink, ignored |
| 0.5 - 1.0 s | Click (optional) |
| 5 - 10 s, then open | Settings & calibration panel |
| 10 s | Suspend tracking |
| 3 deliberate blinks (while suspended) | Wake up |

Sounds at 3 s, 5 s and 10 s tell the user which zone they are in. Full spec, edge cases and
open questions: [docs/gestures.md](docs/gestures.md)

## Getting started

### Requirements

- Windows 10/11 (primary target; Linux/macOS should work for development)
- Python **3.11** (MediaPipe does not support the newest Python versions yet)
- A webcam (not needed for mock mode)

### Install

```powershell
git clone https://github.com/1eminguler/IrisFlow.git
cd IrisFlow
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

For the real engine, also download the face model: see [models/README.md](models/README.md).

### Run

```powershell
python -m irisflow --mock     # mock engine: no camera needed
python -m irisflow            # real webcam engine (not implemented yet)
python -m irisflow --camera 1 # pick another camera
```

**Mock mode controls:** the mouse position is the gaze point, holding **Space** means "eyes
closed", **Esc** quits. Use it to build and test the UI without a camera.

### Test & lint

```powershell
pytest
ruff check .
ruff format .
```

## Project structure

```
IrisFlow/
├── src/irisflow/
│   ├── shared/            # Contract between engine and app  (both)
│   │   ├── types.py       #   GazeFrame, CalibrationSample, CalibrationResult
│   │   ├── interfaces.py  #   GazeEngine protocol
│   │   └── mock_engine.py #   mouse + keyboard fake engine
│   ├── config.py          # Settings + gesture timings       (both)
│   ├── engine/            # Webcam -> GazeFrame              (engine owner)
│   │   ├── camera.py
│   │   ├── iris_tracker.py
│   │   ├── head_pose.py
│   │   ├── blink.py
│   │   ├── calibration.py
│   │   ├── filters.py
│   │   └── webcam_engine.py
│   ├── core/              # Pure-Python app logic            (app owner)
│   │   ├── state_machine.py
│   │   └── dwell.py
│   ├── ui/                # PySide6 screens                  (app owner)
│   ├── services/          # TTS, sounds, OS cursor           (app owner)
│   ├── predict/           # Word prediction                  (flexible)
│   ├── app.py             # Wiring: picks engine, opens window
│   └── __main__.py        # python -m irisflow
├── tests/
├── docs/                  # Architecture & gesture spec
├── models/                # Downloaded model files (not committed)
└── .github/               # CI, PR & issue templates, CODEOWNERS
```

## Team & ownership

| Area | Owner | Responsible for |
|------|-------|-----------------|
| Engine (`engine/`) | _TBD_ | Iris tracking, head-pose compensation, blink detection, calibration math, smoothing, low-power mode |
| App (`core/`, `ui/`, `services/`) | _TBD_ | Gesture state machine, dwell click, calibration screen, need cards, keyboard, settings, TTS, sounds, OS cursor |
| Prediction (`predict/`) | Whoever frees up first | Turkish word prediction for the keyboard |
| Shared (`shared/`, `config.py`) | Both | Changes need both approvals |
| Integration & testing | Both | Real-world tuning, user tests, report, demo |

Workflow rules (branches, PRs, commits): [CONTRIBUTING.md](CONTRIBUTING.md)

## Roadmap

**Phase 0 - Skeleton** ✅
- [x] Project layout, tooling, CI
- [x] Shared contract (`GazeFrame`, `GazeEngine`)
- [x] Mock engine + dev harness window
- [x] Gesture spec

**Phase 1 - Parallel development**
- Engine
  - [ ] Camera capture thread
  - [ ] Iris & eyelid landmarks (MediaPipe)
  - [ ] Blink detection (EAR + hysteresis)
  - [ ] Head-pose compensated eye feature
  - [ ] Calibration fit + save/load
  - [ ] One Euro filter
- App
  - [ ] Gesture state machine + tests
  - [ ] Dwell tracker + dwell ring
  - [ ] Calibration screen
  - [ ] Need cards + TTS
  - [ ] Virtual keyboard
  - [ ] Settings panel, suspended screen, sounds
- Flexible
  - [ ] Word prediction

**Phase 2 - Integration**
- [ ] Real engine replaces mock end to end
- [ ] Tune thresholds with real users (lighting, glasses, distance)
- [ ] OS cursor control outside the app

**Phase 3 - Polish**
- [ ] Windows installer / single executable
- [ ] Accuracy measurements for the report
- [ ] Demo video

## Known limitations

- **Accuracy:** webcam iris tracking is roughly 2-4° accurate, so targets must be large.
- **Lighting:** dim or strongly back-lit rooms reduce accuracy a lot.
- **Glasses:** reflections can confuse the landmark model.
- **Head movement:** small movements are compensated, large ones need recalibration.
- **Some conditions** (e.g. drooping eyelids, nystagmus) may make tracking unreliable.

## Privacy

- All processing happens **locally**. No camera frames leave the computer.
- Frames are processed in memory and **never saved** to disk by default.
- Calibration data and settings are stored only in the user's own profile folder.

## Disclaimer

IrisFlow is a student project and **not a certified medical device**. It must not be the only
way a person can call for help in an emergency.

## License

No license has been chosen yet. Until one is added, all rights are reserved by the authors.
