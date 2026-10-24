# Contributing

We are a two-person team. These rules keep us from stepping on each other's toes.

## Setup

```powershell
git clone https://github.com/1eminguler/IrisFlow.git
cd IrisFlow
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
```

Check that everything works:

```powershell
pytest
python -m irisflow --mock
```

## Branches

- `main` is always working. Nobody pushes to it directly - everything goes through a PR.
- One branch per task, named by area:
  - `engine/iris-tracker`, `engine/one-euro-filter`
  - `app/state-machine`, `app/need-cards`
  - `docs/...`, `chore/...`
- Keep branches short-lived (a few days). Rebase or merge `main` into your branch often.

## Commits

Short, imperative English. No strict format needed, just make it clear:

```
Add EAR-based blink detector
Fix dwell ring not resetting after blink
Tune One Euro filter defaults
```

## Pull requests

1. CI must be green (ruff + pytest).
2. The other person reviews and approves.
3. **Squash and merge**, then delete the branch.

Keep PRs small. A 200-line PR gets a real review, a 2000-line PR gets a rubber stamp.

## Changing the shared contract

`src/irisflow/shared/` and `src/irisflow/config.py` are used by both of us. To change them:

1. Talk first (message / issue) - what changes and why.
2. Make the change in its own small PR, nothing else mixed in.
3. Both of us approve.
4. Update the mock engine and `docs/` in the same PR if needed.

## Code style

- `ruff format .` before committing, `ruff check .` must pass.
- Type hints on public functions.
- Docstrings in English; comments explain *why*, not *what*.
- UI text the user sees is Turkish; code, comments and docs are English.

## Tests

- `core/` and `predict/` logic must have unit tests (they are pure Python - easy to test).
- Engine math (calibration fit, filters, EAR) should have unit tests with synthetic data.
- Tests must never need a camera, a display or network access. CI has none of them.

## Never commit

- Model files (`models/*.task`) - download them, see `models/README.md`.
- Camera recordings or face images - privacy. Use `recordings/` locally, it is git-ignored.
- Personal settings or calibration files.
