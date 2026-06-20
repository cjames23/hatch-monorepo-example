#!/usr/bin/env python3
"""Build every workspace project and collect all artifacts in one folder.

`hatch build` builds a single project (the one rooted at the current working
directory) and writes its wheels/sdists to the location you pass it. This script
builds the root project plus each member under ``packages/`` (skipping the
excluded ``experimental``, mirroring ``workspace.exclude``) into a single shared
output directory at the repo root: ``dist/``.

Usage:
    python scripts/build_all.py            # build into ./dist
    python scripts/build_all.py /tmp/out   # build into a custom directory

Or via Hatch:
    hatch run build:all
    hatch run build:all /tmp/out
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Members under packages/ to skip — mirrors `workspace.exclude` in pyproject.toml.
EXCLUDE = {"experimental"}

# This script lives in <root>/scripts.
ROOT = Path(__file__).resolve().parent.parent


def discover_projects() -> list[Path]:
    """Return the root project followed by every member with a pyproject.toml."""
    projects = [ROOT]
    for child in sorted((ROOT / "packages").iterdir()):
        if child.name in EXCLUDE:
            print(f">>> skipping excluded member: {child.name}")
            continue
        if (child / "pyproject.toml").is_file():
            projects.append(child)
    return projects


def build_env() -> dict[str, str]:
    """Environment for the nested `hatch build` calls.

    When this script runs under `hatch run build:all`, Hatch exports
    HATCH_ENV_ACTIVE=build. The nested `hatch build` would then try to use that
    (non-builder) environment and fail with "is not a builder environment".
    Dropping these makes each build use Hatch's default isolated builder env, so
    the script works both standalone and via `hatch run`.
    """
    env = os.environ.copy()
    env.pop("HATCH_ENV_ACTIVE", None)
    env.pop("HATCH_ENV", None)
    return env


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv

    # Shared output directory (absolute, so it's correct from any project's cwd).
    dist = (ROOT / (argv[0] if argv else "dist")).resolve()
    dist.mkdir(parents=True, exist_ok=True)

    # Clean the shared folder ONCE up front. (Passing `hatch build --clean` per
    # project would instead wipe earlier members' artifacts.)
    for artifact in dist.iterdir():
        if artifact.is_file():
            artifact.unlink()

    env = build_env()
    for project in discover_projects():
        name = "my-app (root)" if project == ROOT else project.name
        print(f">>> building: {name}")
        # Run from inside the project so Hatch picks up its pyproject.toml, and
        # direct the artifacts to the shared output directory.
        subprocess.run(
            ["hatch", "build", str(dist)],
            cwd=project,
            env=env,
            check=True,
        )

    print(f"\nAll artifacts collected in: {dist}")
    for artifact in sorted(dist.iterdir()):
        print(f"  {artifact.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
