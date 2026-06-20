"""`acme_cli` — console entry point tying the workspace members together."""

from __future__ import annotations

import sys

from acme_core import render
from acme_utils import shout

__version__ = "0.1.0"


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    name = argv[0] if argv else "world"
    print(render(shout(name)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
