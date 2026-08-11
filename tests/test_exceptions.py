"""Tests for application-specific exceptions."""

import importlib
import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


def test_exception_module_is_available() -> None:
    assert importlib.util.find_spec("docker_render.exceptions") is not None


@pytest.fixture(scope="module")
def exceptions() -> ModuleType:
    """Load the exception module through its public package path."""
    return importlib.import_module("docker_render.exceptions")


@pytest.mark.parametrize(
    "exception_name",
    [
        "DataDirectoryNotFound",
        "ModuleDirectoryNotFound",
        "ExtensionNotFound",
        "TemplateNotFound",
        "DockerBuildError",
    ],
)
def test_application_exceptions_share_a_common_base(
    exceptions: ModuleType,
    exception_name: str,
) -> None:
    exception_type = getattr(exceptions, exception_name)

    assert issubclass(exception_type, exceptions.DockerRenderError)


@pytest.mark.parametrize(
    ("exception_name", "path", "expected_message"),
    [
        (
            "DataDirectoryNotFound",
            Path("/project/data/9.9"),
            "Data directory not found: /project/data/9.9",
        ),
        (
            "ModuleDirectoryNotFound",
            Path("/project/data/8.4/glibc/modules"),
            "Module directory not found: /project/data/8.4/glibc/modules",
        ),
        (
            "ExtensionNotFound",
            Path("/project/data/8.4/glibc/modules/example.Dockerfile"),
            (
                "Extension file not found: "
                "/project/data/8.4/glibc/modules/example.Dockerfile"
            ),
        ),
        (
            "TemplateNotFound",
            Path("/project/data/8.4/glibc/core.Dockerfile"),
            "Template not found: /project/data/8.4/glibc/core.Dockerfile",
        ),
    ],
)
def test_missing_resource_errors_expose_path_and_meaningful_message(
    exceptions: ModuleType,
    exception_name: str,
    path: Path,
    expected_message: str,
) -> None:
    error = getattr(exceptions, exception_name)(path)

    assert error.path == path
    assert str(error) == expected_message


@pytest.mark.parametrize(
    ("stderr", "expected_message"),
    [
        (
            "permission denied",
            "Docker build failed with exit code 125: permission denied",
        ),
        (
            "first diagnostic line\nsecond diagnostic line\n",
            (
                "Docker build failed with exit code 125: "
                "first diagnostic line\nsecond diagnostic line"
            ),
        ),
        ("", "Docker build failed with exit code 125"),
    ],
)
def test_docker_build_error_exposes_process_details(
    exceptions: ModuleType,
    stderr: str,
    expected_message: str,
) -> None:
    error = exceptions.DockerBuildError(returncode=125, stderr=stderr)

    assert error.returncode == 125
    assert error.stderr == stderr
    assert str(error) == expected_message
