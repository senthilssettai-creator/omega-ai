from typer.testing import CliRunner
from omega.cli import app


def test_status_command():
    runner = CliRunner()
    result = runner.invoke(app, ["status"])
    assert result.exit_code == 0
    assert "Omega is ready" in result.stdout
