"""Application logic for the top-level project.

It composes the workspace members: ``acme_utils.shout`` (which itself builds on
``acme_core.greet``) and ``acme_core.render``. It deliberately relies only on
the members' *core* functionality so it runs in any environment, with or
without the optional member features installed.
"""

from __future__ import annotations

import sys

from acme_core import render
from acme_utils import shout


def run(name: str) -> str:
    """Produce the application's main output line for ``name``."""
    return render(shout(name))


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    name = argv[0] if argv else "world"
    print(run(name))
    return 0
