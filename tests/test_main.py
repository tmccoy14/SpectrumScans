from click.testing import CliRunner
from src.main import cli


def test_version(runner):
    result = runner.invoke(cli, args=["--version"])
    assert not result.exception
    assert result.exit_code == 0
