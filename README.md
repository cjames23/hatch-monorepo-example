# hatch-monorepo-example

A full-featured, **working** reference for [Hatch workspaces](https://hatch.pypa.io/latest/how-to/environment/workspace/):
one repository containing a **top-level project** plus several **workspace
members**, wired together across multiple environments.

It exercises every documented workspace capability:

| Feature | Where it's shown |
| --- | --- |
| Top-level project that is also the workspace root | root [`pyproject.toml`](pyproject.toml) → `my-app` |
| Members by explicit path | `test` env |
| Members by glob (`packages/*`) | `default` env |
| `workspace.exclude` | `default` env excludes `packages/experimental` |
| Per-member `features` (extras) | `test` env: `core` + `pretty`, `utils` + `yaml` |
| `workspace.parallel` | `test` env |
| Inter-member dependencies | `acme-utils` → `acme-core`; `acme-cli` → both |
| Environment-specific member sets | `default` vs `test` vs `lint` |
| Workspace + test matrix | `test` env across Python 3.10/3.11/3.12 |
| Scripts alongside workspace members | `test:run`, `test:cov`, `lint:check` |

## Layout

```
hatch-monorepo-example/
├── pyproject.toml              # top-level project `my-app` + all workspace envs
├── src/my_app/                 # the top-level package
│   ├── __init__.py
│   ├── app.py                  # composes the members
│   └── __main__.py             # `python -m my_app`
├── tests/                      # top-level project's tests
└── packages/                   # the workspace members, each a real project
    ├── core/                   # acme-core   (base lib; extra: pretty -> rich)
    ├── utils/                  # acme-utils  (depends on acme-core; extra: yaml -> PyYAML)
    ├── cli/                    # acme-cli    (depends on core + utils; `acme` script)
    └── experimental/           # acme-experimental  (EXCLUDED from the workspace)
```

Every directory under `packages/` is a standalone project with its own
`pyproject.toml`; each can be built, tested, and published independently.

## How the workspace is wired

Members are declared per-environment under `workspace.members`. Each entry is
either a path, a glob, or a table with `features`:

```toml
# default env: discover everything under packages/, then drop one project
[tool.hatch.envs.default]
workspace.members = ["packages/*"]
workspace.exclude = ["packages/experimental"]

# test env: install members WITH specific extras, in parallel, across Pythons
[tool.hatch.envs.test]
workspace.members = [
    { path = "packages/core", features = ["pretty"] },
    { path = "packages/utils", features = ["yaml"] },
    "packages/cli",
]
workspace.parallel = true
dependencies = ["pytest", "coverage[toml]"]

[[tool.hatch.envs.test.matrix]]
python = ["3.10", "3.11", "3.12"]
```

Members are installed as **editable** packages, so edits to a member's source
are picked up immediately with no re-install.

### Why the root project lists no members in `[project].dependencies`

Hatch installs the **root** project editable *before* it syncs the workspace
members. If the root listed `acme-core` as a hard dependency, pip would try to
resolve it from PyPI at that first step (and fail). Inside the workspace the
members are provided by `workspace.members`, and `my_app` imports them from
there.

Members that depend on *each other* (e.g. `acme-utils` → `acme-core`) **do**
declare those dependencies normally — all members are installed together in a
single step, so pip resolves the local editable copies.

## Try it

```bash
# default env — glob members, experimental excluded
hatch run my-app Hatch
#> HELLO, HATCH!

# the acme CLI from the acme-cli member
hatch run acme monorepo
#> HELLO, MONOREPO!

# run the test suite across the whole matrix (3.10 / 3.11 / 3.12)
hatch run test:run

# run a single matrix entry
hatch run test.py3.12:run

# coverage
hatch run test:cov

# lint (reduced member set + ruff, which is a normal dependency, not a member)
hatch run lint:check

# inspect the environments and their members
hatch env show
```

## Building all members into one folder

`hatch build` builds a single project (the one rooted at the current directory)
and writes its artifacts to the location you pass it. To build the **whole
monorepo** and collect every wheel/sdist in one place, build each project in
turn into a shared output directory.

[`scripts/build_all.py`](scripts/build_all.py) does exactly that — it builds the
root project plus every member (skipping the excluded `experimental`, mirroring
`workspace.exclude`) into a single top-level `dist/`. It's a small, cross-platform
Python helper that discovers the members dynamically, so it never drifts from the
package set:

```bash
python scripts/build_all.py            # -> ./dist
python scripts/build_all.py /tmp/out   # -> custom directory

# or via the `build` environment:
hatch run build:all
hatch run build:all /tmp/out
```

Result — one folder with every project's artifacts:

```
dist/
├── my_app-0.1.0-py3-none-any.whl
├── my_app-0.1.0.tar.gz
├── acme_core-0.1.0-py3-none-any.whl
├── acme_core-0.1.0.tar.gz
├── acme_utils-0.1.0-py3-none-any.whl
├── acme_utils-0.1.0.tar.gz
├── acme_cli-0.1.0-py3-none-any.whl
└── acme_cli-0.1.0.tar.gz
```

The key idea is that `hatch build dist/` (an explicit output **location**) lets
every project target the same directory; the script cleans that directory once
up front rather than per-project, so earlier members' artifacts aren't wiped.

> Requires Hatch with workspace support (`hatch >= 1.16`). The `test` matrix
> needs Python 3.10, 3.11, and 3.12 available to Hatch; trim the matrix in
> `pyproject.toml` if you only have some of them.
