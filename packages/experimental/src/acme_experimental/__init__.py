"""`acme_experimental` — excluded from the workspace via `workspace.exclude`."""

__version__ = "0.0.1"


def experiment() -> str:
    return "this package is excluded from the default workspace environment"
