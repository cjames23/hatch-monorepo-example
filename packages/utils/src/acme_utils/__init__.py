"""`acme_utils` — helpers layered on top of :mod:`acme_core`."""

from __future__ import annotations

from acme_core import greet

__version__ = "0.1.0"


def shout(name: str) -> str:
    """Return an emphatic greeting, reusing :func:`acme_core.greet`."""
    return greet(name).upper()


def parse_config(text: str) -> dict:
    """Parse a small YAML document.

    Requires the optional ``yaml`` extra (``PyYAML``). In the ``test``
    environment ``acme-utils`` is installed with ``features = ["yaml"]``.
    """
    import yaml

    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        msg = "expected a YAML mapping"
        raise ValueError(msg)
    return data
