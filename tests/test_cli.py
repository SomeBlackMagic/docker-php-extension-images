"""Smoke tests for the command-line interface."""

import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner

import docker_render.cli as cli_module
from docker_render.cli import cli
from docker_render.exceptions import DockerBuildError

DEFAULT_IMAGE = "someblackmagic/docker-php-extension-images"


def write_render_inputs(base_path: Path) -> None:
    data_directory = base_path / "data" / "8.4" / "glibc"
    modules_directory = data_directory / "modules"
    modules_directory.mkdir(parents=True)
    (data_directory / "core.Dockerfile").write_text(
        "FROM scratch\n{{ module | raw }}",
        encoding="utf-8",
    )
    (modules_directory / "redis.Dockerfile").write_text(
        "RUN printf 'Grüße — 你好'\n",
        encoding="utf-8",
    )


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


def test_render_one_writes_dockerfile_and_runs_expected_build(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(
        cli_module,
        "run_docker_build",
        run_docker_build,
        raising=False,
    )

    result = CliRunner().invoke(cli, ["render-one", "8.4", "glibc", "redis"])

    dockerfile = tmp_path / "dst" / "8.4" / "glibc" / "redis.Dockerfile"
    assert result.exit_code == 0
    assert dockerfile.read_text(encoding="utf-8") == (
        "FROM scratch\nRUN printf 'Grüße — 你好'\n"
    )
    run_docker_build.assert_called_once_with(
        [
            "docker",
            "buildx",
            "build",
            "--platform",
            "linux/amd64,linux/arm64",
            "--progress",
            "plain",
            "--push",
            "--tag",
            f"{DEFAULT_IMAGE}:8.4-redis-glibc",
            "--file",
            str(dockerfile),
            str(dockerfile.parent),
        ],
        verbose=True,
    )


def test_render_one_uses_configured_image_repository(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(
        cli_module,
        "run_docker_build",
        run_docker_build,
        raising=False,
    )

    result = CliRunner().invoke(
        cli,
        [
            "render-one",
            "--image",
            "registry.example.com/php-extensions",
            "8.4",
            "glibc",
            "redis",
        ],
    )

    assert result.exit_code == 0
    command = run_docker_build.call_args.args[0]
    assert "registry.example.com/php-extensions:8.4-redis-glibc" in command


def test_render_one_reports_the_exact_missing_extension(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    run_docker_build = Mock()
    monkeypatch.setattr(
        cli_module,
        "run_docker_build",
        run_docker_build,
        raising=False,
    )

    result = CliRunner().invoke(cli, ["render-one", "8.4", "glibc", "missing"])

    missing_module = (
        tmp_path / "data" / "8.4" / "glibc" / "modules" / ("missing.Dockerfile")
    )
    assert result.exit_code != 0
    assert f"Extension file not found: {missing_module}" in result.output
    run_docker_build.assert_not_called()


def test_render_one_preserves_docker_failure_exit_code(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(
        cli_module,
        "run_docker_build",
        Mock(
            side_effect=DockerBuildError(
                returncode=125,
                stderr="docker daemon unavailable",
            )
        ),
        raising=False,
    )

    result = CliRunner().invoke(cli, ["render-one", "8.4", "glibc", "redis"])

    assert result.exit_code == 125
    assert "Docker build failed with exit code 125" in result.output
    assert "docker daemon unavailable" in result.output
