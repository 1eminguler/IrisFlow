"""Entry point: ``python -m irisflow`` or the ``irisflow`` command."""

from __future__ import annotations

import sys

from irisflow.app import run


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
