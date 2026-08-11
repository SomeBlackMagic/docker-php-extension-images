"""Tests for Docker subprocess execution."""

import importlib
import importlib.util
import subprocess
from types import ModuleType
from unittest.mock import Mock

import pytest

from docker_render.exceptions import DockerBuildError

RUNNER_MODULE_NAME = "docker_render.docker_runner"
RUNNER_MODULE_EXISTS = importlib.util.find_spec(RUNNER_MODULE_NAME) is not None


def test_docker_runner_module_exists() -> None:
    assert RUNNER_MODULE_EXISTS


@pytest.fixture
def docker_runner() -> ModuleType:
    if not RUNNER_MODULE_EXISTS:
        pytest.skip(f"{RUNNER_MODULE_NAME} is not implemented yet")

    return importlib.import_module(RUNNER_MODULE_NAME)


def test_runs_structured_command_and_captures_output_by_default(
    docker_runner: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = ["docker", "buildx", "build", "--file", "build context/Dockerfile", "."]
    run = Mock(return_value=subprocess.CompletedProcess(command, 0, "built", ""))
    monkeypatch.setattr(docker_runner.subprocess, "run", run)

    result = docker_runner.run_docker_build(command)

    assert result is None
    run.assert_called_once_with(
        command,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )


def test_verbose_mode_streams_output_without_capturing_it(
    docker_runner: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = ["docker", "buildx", "build", "."]
    run = Mock(return_value=subprocess.CompletedProcess(command, 0))
    monkeypatch.setattr(docker_runner.subprocess, "run", run)

    docker_runner.run_docker_build(command, verbose=True)

    run.assert_called_once_with(
        command,
        check=False,
        capture_output=False,
        text=True,
        shell=False,
    )


def test_raises_typed_error_with_process_details_on_failure(
    docker_runner: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = ["docker", "buildx", "build", "."]
    run = Mock(
        return_value=subprocess.CompletedProcess(
            command,
            125,
            stdout="partial output",
            stderr="docker daemon unavailable",
        )
    )
    monkeypatch.setattr(docker_runner.subprocess, "run", run)

    with pytest.raises(DockerBuildError) as raised:
        docker_runner.run_docker_build(command)

    assert raised.value.returncode == 125
    assert raised.value.stderr == "docker daemon unavailable"


def test_verbose_failure_preserves_exit_code_without_captured_stderr(
    docker_runner: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    command = ["docker", "buildx", "build", "."]
    run = Mock(return_value=subprocess.CompletedProcess(command, 17))
    monkeypatch.setattr(docker_runner.subprocess, "run", run)

    with pytest.raises(DockerBuildError) as raised:
        docker_runner.run_docker_build(command, verbose=True)

    assert raised.value.returncode == 17
    assert raised.value.stderr == ""
