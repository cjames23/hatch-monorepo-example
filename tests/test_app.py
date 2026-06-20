from my_app.app import run


def test_run_composes_members():
    assert "HELLO, MONOREPO!" in run("monorepo")
