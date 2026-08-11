"""Tests for deterministic Docker Buildx command construction."""

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

import pytest

BUILDER_MODULE_NAME = "docker_render.builder"
BUILDER_MODULE_EXISTS = find_spec(BUILDER_MODULE_NAME) is not None


def test_builder_module_exists() -> None:
    assert BUILDER_MODULE_EXISTS


@pytest.fixture
def builder() -> ModuleType:
    if not BUILDER_MODULE_EXISTS:
        pytest.skip(f"{BUILDER_MODULE_NAME} is not implemented yet")

    return import_module(BUILDER_MODULE_NAME)


def test_builds_image_tag(builder: ModuleType) -> None:
    assert (
        builder.build_image_tag(
            image="registry.example.com/php-extensions",
            version="8.4",
            extension="pdo_pgsql",
            os_variant="musl",
        )
        == "registry.example.com/php-extensions:8.4-pdo_pgsql-musl"
    )


def test_builds_batch_command_with_pull(builder: ModuleType, tmp_path: Path) -> None:
    dockerfile = tmp_path / "dst" / "8.4" / "glibc" / "redis.Dockerfile"
    context = dockerfile.parent

    command = builder.build_docker_command(
        image="someblackmagic/docker-php-extension-images",
        version="8.4",
        extension="redis",
        os_variant="glibc",
        dockerfile=dockerfile,
        context=context,
        pull=True,
    )

    assert command == [
        "docker",
        "buildx",
        "build",
        "--platform",
        "linux/amd64,linux/arm64",
        "--push",
        "--pull",
        "--tag",
        "someblackmagic/docker-php-extension-images:8.4-redis-glibc",
        "--file",
        str(dockerfile),
        str(context),
    ]


def test_builds_single_extension_command_with_plain_progress(
    builder: ModuleType,
    tmp_path: Path,
) -> None:
    dockerfile = tmp_path / "dst" / "8.5" / "musl" / "xdebug.Dockerfile"
    context = dockerfile.parent

    command = builder.build_docker_command(
        image="example/php-extensions",
        version="8.5",
        extension="xdebug",
        os_variant="musl",
        dockerfile=dockerfile,
        context=context,
        progress_plain=True,
    )

    assert command == [
        "docker",
        "buildx",
        "build",
        "--platform",
        "linux/amd64,linux/arm64",
        "--progress",
        "plain",
        "--push",
        "--tag",
        "example/php-extensions:8.5-xdebug-musl",
        "--file",
        str(dockerfile),
        str(context),
    ]


@pytest.mark.parametrize(
    ("pull", "progress_plain", "expected_optional_arguments"),
    [
        (False, False, []),
        (True, False, ["--pull"]),
        (False, True, ["--progress", "plain"]),
        (True, True, ["--progress", "plain", "--pull"]),
    ],
)
def test_supports_optional_flag_combinations(
    builder: ModuleType,
    tmp_path: Path,
    pull: bool,
    progress_plain: bool,
    expected_optional_arguments: list[str],
) -> None:
    command = builder.build_docker_command(
        image="example/php-extensions",
        version="8.3",
        extension="amqp",
        os_variant="glibc",
        dockerfile=tmp_path / "amqp.Dockerfile",
        context=tmp_path,
        pull=pull,
        progress_plain=progress_plain,
    )

    optional_arguments = [
        argument
        for argument in command
        if argument in {"--progress", "plain", "--pull"}
    ]
    assert optional_arguments == expected_optional_arguments


def test_keeps_paths_with_spaces_as_individual_arguments(
    builder: ModuleType,
    tmp_path: Path,
) -> None:
    context = tmp_path / "build context"
    dockerfile = context / "redis extension.Dockerfile"

    command = builder.build_docker_command(
        image="example/php-extensions",
        version="8.2",
        extension="redis",
        os_variant="musl",
        dockerfile=dockerfile,
        context=context,
    )

    assert command[command.index("--file") + 1] == str(dockerfile)
    assert command[-1] == str(context)
    assert str(dockerfile) in command
    assert str(context) in command


def test_command_construction_has_no_filesystem_side_effects(
    builder: ModuleType,
    tmp_path: Path,
) -> None:
    context = tmp_path / "missing context"
    dockerfile = context / "missing.Dockerfile"

    builder.build_docker_command(
        image="example/php-extensions",
        version="8.1",
        extension="missing",
        os_variant="glibc",
        dockerfile=dockerfile,
        context=context,
    )

    assert list(tmp_path.iterdir()) == []
