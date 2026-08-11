"""Tests for repository path resolution."""

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

import pytest

PATHS_MODULE_NAME = "docker_render.paths"
PATHS_MODULE_EXISTS = find_spec(PATHS_MODULE_NAME) is not None


def test_paths_module_exists() -> None:
    assert PATHS_MODULE_EXISTS


@pytest.fixture
def paths() -> ModuleType:
    if not PATHS_MODULE_EXISTS:
        pytest.skip(f"{PATHS_MODULE_NAME} is not implemented yet")

    return import_module(PATHS_MODULE_NAME)


def test_repository_root_is_resolved_from_package_location(paths: ModuleType) -> None:
    expected_root = Path(paths.__file__).resolve().parents[1]

    assert paths.repository_root() == expected_root


def test_repository_root_uses_explicit_base_path(
    paths: ModuleType,
    tmp_path: Path,
) -> None:
    assert paths.repository_root(tmp_path) == tmp_path


@pytest.mark.parametrize(
    ("version", "os_variant"),
    [
        ("7.4", "glibc"),
        ("8.4", "musl"),
    ],
)
def test_resolves_input_directories(
    paths: ModuleType,
    tmp_path: Path,
    version: str,
    os_variant: str,
) -> None:
    assert paths.data_directory(version, os_variant, tmp_path) == (
        tmp_path / "data" / version / os_variant
    )
    assert paths.modules_directory(version, os_variant, tmp_path) == (
        tmp_path / "data" / version / os_variant / "modules"
    )


@pytest.mark.parametrize("extension", ["redis", "pdo_pgsql"])
def test_resolves_input_files(
    paths: ModuleType,
    tmp_path: Path,
    extension: str,
) -> None:
    assert paths.module_file("8.5", "musl", extension, tmp_path) == (
        tmp_path / "data" / "8.5" / "musl" / "modules" / f"{extension}.Dockerfile"
    )
    assert paths.core_template("8.5", "musl", tmp_path) == (
        tmp_path / "data" / "8.5" / "musl" / "core.Dockerfile"
    )


@pytest.mark.parametrize(
    ("version", "os_variant", "extension"),
    [
        ("7.4", "glibc", "amqp"),
        ("8.5", "musl", "pdo_pgsql"),
    ],
)
def test_resolves_output_paths(
    paths: ModuleType,
    tmp_path: Path,
    version: str,
    os_variant: str,
    extension: str,
) -> None:
    assert paths.destination_directory(version, os_variant, tmp_path) == (
        tmp_path / "dst" / version / os_variant
    )
    assert paths.generated_dockerfile(version, os_variant, extension, tmp_path) == (
        tmp_path / "dst" / version / os_variant / f"{extension}.Dockerfile"
    )
    assert paths.builder_script(version, os_variant, tmp_path) == (
        tmp_path / "dst" / f"builder-{version}-{os_variant}.sh"
    )


def test_all_path_functions_return_path_instances(
    paths: ModuleType,
    tmp_path: Path,
) -> None:
    resolved_paths = [
        paths.repository_root(tmp_path),
        paths.data_directory("8.4", "glibc", tmp_path),
        paths.modules_directory("8.4", "glibc", tmp_path),
        paths.module_file("8.4", "glibc", "xdebug", tmp_path),
        paths.core_template("8.4", "glibc", tmp_path),
        paths.destination_directory("8.4", "glibc", tmp_path),
        paths.generated_dockerfile("8.4", "glibc", "xdebug", tmp_path),
        paths.builder_script("8.4", "glibc", tmp_path),
    ]

    assert all(isinstance(path, Path) for path in resolved_paths)


def test_path_resolution_does_not_create_files_or_directories(
    paths: ModuleType,
    tmp_path: Path,
) -> None:
    paths.module_file("8.5", "musl", "redis", tmp_path)
    paths.generated_dockerfile("8.5", "musl", "redis", tmp_path)
    paths.builder_script("8.5", "musl", tmp_path)

    assert list(tmp_path.iterdir()) == []
