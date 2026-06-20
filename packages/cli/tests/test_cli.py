from acme_cli import main


def test_cli_runs(capsys):
    exit_code = main(["acme"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "HELLO, ACME!" in captured.out
