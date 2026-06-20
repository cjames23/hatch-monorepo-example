# acme-experimental

A project under `packages/` that is deliberately **excluded** from the
workspace via `workspace.exclude = ["packages/experimental"]` in the root
`pyproject.toml`. It demonstrates how to keep a project in the monorepo without
installing it into the shared environment.
