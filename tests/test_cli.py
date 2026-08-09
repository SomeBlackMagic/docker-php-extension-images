"""Smoke tests for the command-line interface."""

import subprocess
import sys
from pathlib import Path

from click.testing import CliRunner

from docker_render.cli import cli


def test_cli_help() -> None:
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Render and build Docker PHP extension images." in result.output


def test_compatibility_launcher_help() -> None:
    repository_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [sys.executable, repository_root / "render", "--help"],
        cwd=repository_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Render and build Docker PHP extension images." in result.stdout
