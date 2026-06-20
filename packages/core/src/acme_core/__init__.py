"""`acme_core` — the base library shared by every other workspace member."""

from __future__ import annotations

__version__ = "0.1.0"


def greet(name: str) -> str:
    """Return a plain greeting for ``name``."""
    return f"Hello, {name}!"


def render(text: str) -> str:
    """Render ``text``, using ``rich`` markup when the ``pretty`` extra is installed.

    This demonstrates per-member *features*: in the ``test`` environment
    ``acme-core`` is installed with ``features = ["pretty"]`` so ``rich`` is
    importable; in a bare install it gracefully degrades to plain text.
    """
    try:
        from rich.console import Console
    except ImportError:
        return text

    console = Console(no_color=True)
    with console.capture() as capture:
        console.print(f"[bold]{text}[/bold]", end="")
    return capture.get()


def has_pretty() -> bool:
    """Return ``True`` when the optional ``pretty`` extra (``rich``) is available."""
    try:
        import rich  # noqa: F401
    except ImportError:
        return False
    return True
