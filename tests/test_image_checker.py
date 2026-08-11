"""Tests for local and remote Docker image inspection."""

import importlib
import importlib.util
import subprocess
from types import ModuleType
from unittest.mock import Mock, call

import pytest

CHECKER_MODULE_NAME = "docker_render.image_checker"
CHECKER_MODULE_EXISTS = importlib.util.find_spec(CHECKER_MODULE_NAME) is not None


def test_image_checker_module_exists() -> None:
    assert CHECKER_MODULE_EXISTS


@pytest.fixture
def image_checker() -> ModuleType:
    if not CHECKER_MODULE_EXISTS:
        pytest.skip(f"{CHECKER_MODULE_NAME} is not implemented yet")

    return importlib.import_module(CHECKER_MODULE_NAME)


def test_remote_image_is_the_authoritative_skip_condition(
    image_checker: ModuleType,
) -> None:
    status = image_checker.ImageStatus(remote_exists=True, local_exists=False)

    assert status.should_skip is True


def test_local_image_alone_does_not_skip_build(
    image_checker: ModuleType,
) -> None:
    status = image_checker.ImageStatus(remote_exists=False, local_exists=True)

    assert status.should_skip is False


def test_inspects_remote_and_local_images_with_structured_commands(
    image_checker: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = "registry.example.com/php-extensions:8.4-redis-glibc"
    run = Mock(
        side_effect=[
            subprocess.CompletedProcess([], 0, stdout="{}", stderr=""),
            subprocess.CompletedProcess([], 1, stdout="[]", stderr="No such image"),
        ]
    )
    monkeypatch.setattr(image_checker.subprocess, "run", run)

    status = image_checker.check_image_status(image)

    assert status.remote_exists is True
    assert status.local_exists is False
    assert status.local_error is None
    assert run.call_args_list == [
        call(
            ["docker", "manifest", "inspect", image],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        ),
        call(
            ["docker", "image", "inspect", image],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
        ),
    ]


def test_confirmed_missing_remote_manifest_is_a_normal_status(
    image_checker: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = "registry.example.com/php-extensions:8.4-redis-glibc"
    run = Mock(
        side_effect=[
            subprocess.CompletedProcess(
                [],
                1,
                stdout="",
                stderr="manifest unknown: manifest unknown",
            ),
            subprocess.CompletedProcess([], 0, stdout="[]", stderr=""),
        ]
    )
    monkeypatch.setattr(image_checker.subprocess, "run", run)

    status = image_checker.check_image_status(image)

    assert status.remote_exists is False
    assert status.local_exists is True
    assert status.should_skip is False


def test_unexpected_remote_inspection_failure_is_not_reported_as_missing(
    image_checker: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = "registry.example.com/php-extensions:8.4-redis-glibc"
    run = Mock(
        return_value=subprocess.CompletedProcess(
            [],
            1,
            stdout="",
            stderr="unauthorized: authentication required",
        )
    )
    monkeypatch.setattr(image_checker.subprocess, "run", run)

    with pytest.raises(image_checker.ImageInspectionError) as raised:
        image_checker.check_image_status(image)

    assert raised.value.image == image
    assert raised.value.returncode == 1
    assert "authentication required" in str(raised.value)
    assert run.call_count == 1


def test_local_inspection_failure_is_available_for_diagnostics(
    image_checker: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    image = "registry.example.com/php-extensions:8.4-redis-glibc"
    run = Mock(
        side_effect=[
            subprocess.CompletedProcess(
                [],
                1,
                stdout="",
                stderr="no such manifest: registry.example.com/php-extensions",
            ),
            subprocess.CompletedProcess(
                [],
                125,
                stdout="",
                stderr="Cannot connect to the Docker daemon",
            ),
        ]
    )
    monkeypatch.setattr(image_checker.subprocess, "run", run)

    status = image_checker.check_image_status(image)

    assert status.remote_exists is False
    assert status.local_exists is None
    assert status.local_error == "Cannot connect to the Docker daemon"
    assert status.should_skip is False
