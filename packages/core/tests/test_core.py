from acme_core import greet, has_pretty, render


def test_greet():
    assert greet("world") == "Hello, world!"


def test_render_returns_text():
    # Works whether or not the `pretty` extra is installed.
    assert "hi" in render("hi")


def test_pretty_feature_installed():
    # In the `test` environment acme-core is installed with features=["pretty"],
    # so `rich` must be importable.
    assert has_pretty() is True
