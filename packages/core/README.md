# acme-core

Base library for the ACME monorepo and a **workspace member**.

Standalone project (own `pyproject.toml`, independently buildable/publishable),
also listed as a member in the root `pyproject.toml`. Provides an optional
`pretty` extra (`rich`) that is enabled per-environment via the member
`features` option.
