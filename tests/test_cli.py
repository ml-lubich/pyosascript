"""
Tests for pyosascript CLI commands.
"""

from typer.testing import CliRunner
from pyosascript.cli import app

runner = CliRunner()


def test_cli_version():
    res = runner.invoke(app, ["version"])
    assert res.exit_code == 0
    assert "pyosascript" in res.stdout


def test_cli_eval():
    res = runner.invoke(app, ["eval", "return 10 + 20"])
    assert res.exit_code == 0
    assert "30" in res.stdout


def test_cli_eval_json():
    res = runner.invoke(app, ["eval", "return 42", "-j"])
    assert res.exit_code == 0
    assert '"ok": true' in res.stdout
    assert '"returncode": 0' in res.stdout


def test_cli_eval_jxa():
    res = runner.invoke(app, ["eval", "(() => 5 * 5)()", "-l", "JavaScript"])
    assert res.exit_code == 0
    assert "25" in res.stdout
