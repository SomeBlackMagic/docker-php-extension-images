"""Smoke tests for the command-line interface."""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import Mock

import pytest
from click.testing import CliRunner

import docker_render.cli as cli_module
from docker_render.cli import cli
from docker_render.exceptions import DockerBuildError

DEFAULT_IMAGE = "someblackmagic/docker-php-extension-images"


@dataclass(frozen=True)
class StubImageStatus:
    remote_exists: bool
    local_exists: bool | None = None
    local_error: str | None = None

    @property
    def should_skip(self) -> bool:
        return self.remote_exists


@pytest.fixture(autouse=True)
def images_are_missing_by_default(monkeypatch: pytest.MonkeyPatch) -> Mock:
    check_image_status = Mock(
        return_value=StubImageStatus(remote_exists=False, local_exists=False)
    )
    monkeypatch.setattr(
        cli_module,
        "check_image_status",
        check_image_status,
        raising=False,
    )
    return check_image_status


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


def invoke_batch_render(tmp_path: Path, monkeypatch, *arguments: str):
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    return CliRunner().invoke(cli, ["render", *arguments])


def test_aggregate_writes_configured_extensions_to_var_dockerfile(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template_path = tmp_path / "templates" / "aggregate.Dockerfile"
    template_path.parent.mkdir(parents=True)
    template_path.write_text(
        "FROM php:{{ version }}-{{ base_os }}\n"
        "{% for image_tag in image_tags %}COPY --from={{ image_tag }} / /\n{% endfor %}",
        encoding="utf-8",
    )
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)

    result = CliRunner().invoke(
        cli,
        [
            "aggregate",
            "--image",
            "registry.example.com/php-extensions",
            "7.4",
            "musl",
            "redis",
            "http",
        ],
    )

    output_path = tmp_path / "var" / "Dockerfile"
    assert result.exit_code == 0
    assert output_path.read_text(encoding="utf-8") == (
        "FROM php:7.4-alpine\n"
        "COPY --from=registry.example.com/php-extensions:7.4-redis-musl / /\n"
        "COPY --from=registry.example.com/php-extensions:7.4-http-musl / /\n"
    )
    assert result.output == f"Rendered aggregate Dockerfile: {output_path}\n"


def test_aggregate_rejects_missing_extensions_without_writing_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template_path = tmp_path / "templates" / "aggregate.Dockerfile"
    template_path.parent.mkdir(parents=True)
    template_path.write_text("FROM scratch\n", encoding="utf-8")
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)

    result = CliRunner().invoke(cli, ["aggregate", "8.4", "musl"])

    assert result.exit_code != 0
    assert "Missing argument 'EXTENSIONS...'" in result.output
    assert not (tmp_path / "var" / "Dockerfile").exists()


def test_cli_help() -> None:
    result = CliRunner().invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Render and build Docker PHP extension images." in result.output
    assert "-v, --verbose" in result.output


def test_verbose_mode_reports_workflow_progress(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)

    result = CliRunner().invoke(cli, ["-v", "render", "8.4", "glibc"])

    assert result.exit_code == 0
    assert "INFO docker_render.cli: Starting batch render" in result.output
    assert "INFO docker_render.cli: Processing extension redis" in result.output
    assert "INFO docker_render.builder: Wrote executable builder script" in result.output


def test_double_verbose_mode_reports_diagnostics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)

    result = CliRunner().invoke(cli, ["-vv", "render", "8.4", "glibc"])

    assert result.exit_code == 0
    assert "DEBUG docker_render.cli: Image status" in result.output
    assert "DEBUG docker_render.builder: Constructed Docker command" in result.output


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
            "--cache-from",
            f"type=registry,ref={DEFAULT_IMAGE}:buildcache-8.4-redis-glibc",
            "--cache-to",
            f"type=registry,ref={DEFAULT_IMAGE}:buildcache-8.4-redis-glibc,mode=max",
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


def test_render_one_uses_custom_cache_reference(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    cache_ref = "registry.example.com/cache/php:redis"
    result = CliRunner().invoke(
        cli,
        [
            "render-one",
            "--cache-ref",
            cache_ref,
            "8.4",
            "glibc",
            "redis",
        ],
    )

    assert result.exit_code == 0
    command = run_docker_build.call_args.args[0]
    assert f"type=registry,ref={cache_ref}" in command
    assert f"type=registry,ref={cache_ref},mode=max" in command


def test_render_one_no_cache_omits_registry_cache_arguments(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    result = CliRunner().invoke(
        cli,
        ["render-one", "--no-cache", "8.4", "glibc", "redis"],
    )

    assert result.exit_code == 0
    command = run_docker_build.call_args.args[0]
    assert "--cache-from" not in command
    assert "--cache-to" not in command


def test_render_one_rejects_cache_reference_when_cache_is_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    result = CliRunner().invoke(
        cli,
        [
            "render-one",
            "--no-cache",
            "--cache-ref",
            "registry.example.com/cache/php:redis",
            "8.4",
            "glibc",
            "redis",
        ],
    )

    assert result.exit_code != 0
    assert "--no-cache cannot be used with --cache-ref" in result.output
    run_docker_build.assert_not_called()
    assert not (tmp_path / "dst").exists()


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


def test_render_one_skips_remotely_existing_image(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    images_are_missing_by_default: Mock,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    images_are_missing_by_default.return_value = StubImageStatus(
        remote_exists=True,
        local_exists=False,
    )
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    result = CliRunner().invoke(cli, ["render-one", "8.4", "glibc", "redis"])

    image = f"{DEFAULT_IMAGE}:8.4-redis-glibc"
    assert result.exit_code == 0
    assert result.output == f"[SKIP] {image}\n"
    images_are_missing_by_default.assert_called_once_with(image)
    run_docker_build.assert_not_called()
    assert not (tmp_path / "dst").exists()


def test_render_one_builds_when_image_exists_only_locally(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    images_are_missing_by_default: Mock,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    images_are_missing_by_default.return_value = StubImageStatus(
        remote_exists=False,
        local_exists=True,
    )
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    result = CliRunner().invoke(cli, ["render-one", "8.4", "glibc", "redis"])

    image = f"{DEFAULT_IMAGE}:8.4-redis-glibc"
    assert result.exit_code == 0
    assert f"[BUILD] {image}\n" in result.output
    run_docker_build.assert_called_once()


@pytest.mark.parametrize("force_option", ["--force", "-f"])
def test_render_one_force_builds_without_inspecting_image(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    images_are_missing_by_default: Mock,
    force_option: str,
) -> None:
    write_render_inputs(tmp_path)
    monkeypatch.setattr(cli_module, "repository_root", lambda: tmp_path, raising=False)
    run_docker_build = Mock()
    monkeypatch.setattr(cli_module, "run_docker_build", run_docker_build)

    result = CliRunner().invoke(
        cli,
        ["render-one", force_option, "8.4", "glibc", "redis"],
    )

    assert result.exit_code == 0
    images_are_missing_by_default.assert_not_called()
    run_docker_build.assert_called_once()


def test_render_batch_writes_sorted_dockerfiles_and_builder_script(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    modules_directory = tmp_path / "data" / "8.4" / "glibc" / "modules"
    (modules_directory / "amqp.Dockerfile").write_text(
        "RUN install-amqp\n",
        encoding="utf-8",
    )
    (modules_directory / ".DS_Store").write_text("metadata", encoding="utf-8")
    (modules_directory / "notes.txt").write_text("notes", encoding="utf-8")
    (modules_directory / "nested.Dockerfile").mkdir()

    result = invoke_batch_render(tmp_path, monkeypatch, "8.4", "glibc")

    destination = tmp_path / "dst" / "8.4" / "glibc"
    assert result.exit_code == 0
    assert (destination / "amqp.Dockerfile").read_text(encoding="utf-8") == (
        "FROM scratch\nRUN install-amqp\n"
    )
    assert (destination / "redis.Dockerfile").read_text(encoding="utf-8") == (
        "FROM scratch\nRUN printf 'Grüße — 你好'\n"
    )
    builder_script = tmp_path / "dst" / "builder-8.4-glibc.sh"
    builder_lines = builder_script.read_text(encoding="utf-8").splitlines()
    assert builder_lines[:2] == ["#!/usr/bin/env bash", "set -euo pipefail"]
    assert len(builder_lines) == 4
    assert "8.4-amqp-glibc" in builder_lines[2]
    assert "8.4-redis-glibc" in builder_lines[3]
    assert all("--pull" in line for line in builder_lines[2:])
    assert all("--progress plain" not in line for line in builder_lines[2:])
    assert result.output == "Rendered: 2, skipped: 3\n"


def test_render_batch_uses_configured_image_and_replaces_stale_builder(
    tmp_path: Path,
    monkeypatch,
) -> None:
    write_render_inputs(tmp_path)
    builder_script = tmp_path / "dst" / "builder-8.4-glibc.sh"
    builder_script.parent.mkdir(parents=True)
    builder_script.write_text("stale command\n", encoding="utf-8")

    result = invoke_batch_render(
        tmp_path,
        monkeypatch,
        "--image",
        "registry.example.com/php-extensions",
        "8.4",
        "glibc",
    )

    assert result.exit_code == 0
    content = builder_script.read_text(encoding="utf-8")
    assert "registry.example.com/php-extensions:8.4-redis-glibc" in content
    assert "stale command" not in content


def test_render_batch_expands_cache_reference_template_per_extension(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)
    modules_directory = tmp_path / "data" / "8.4" / "glibc" / "modules"
    (modules_directory / "amqp.Dockerfile").write_text(
        "RUN install-amqp\n",
        encoding="utf-8",
    )

    result = invoke_batch_render(
        tmp_path,
        monkeypatch,
        "--image",
        "registry.example.com/php-extensions",
        "--cache-ref",
        "{image}:cache-{version}-{ext}-{os}",
        "8.4",
        "glibc",
    )

    assert result.exit_code == 0
    script = (tmp_path / "dst" / "builder-8.4-glibc.sh").read_text(encoding="utf-8")
    for extension in ("amqp", "redis"):
        cache_ref = f"registry.example.com/php-extensions:cache-8.4-{extension}-glibc"
        assert f"type=registry,ref={cache_ref}" in script
        assert f"type=registry,ref={cache_ref},mode=max" in script


def test_render_batch_rejects_unknown_cache_reference_placeholder(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)

    result = invoke_batch_render(
        tmp_path,
        monkeypatch,
        "--cache-ref",
        "{image}:cache-{unknown}",
        "8.4",
        "glibc",
    )

    assert result.exit_code != 0
    assert "Unknown cache reference placeholder: unknown" in result.output
    assert not (tmp_path / "dst").exists()


def test_render_batch_rejects_cache_reference_when_cache_is_disabled(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_render_inputs(tmp_path)

    result = invoke_batch_render(
        tmp_path,
        monkeypatch,
        "--no-cache",
        "--cache-ref",
        "{image}:cache-{ext}",
        "8.4",
        "glibc",
    )

    assert result.exit_code != 0
    assert "--no-cache cannot be used with --cache-ref" in result.output
    assert not (tmp_path / "dst").exists()


def test_render_batch_reports_build_and_skip_decisions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    images_are_missing_by_default: Mock,
) -> None:
    write_render_inputs(tmp_path)
    modules_directory = tmp_path / "data" / "8.4" / "glibc" / "modules"
    (modules_directory / "amqp.Dockerfile").write_text(
        "RUN install-amqp\n",
        encoding="utf-8",
    )
    images_are_missing_by_default.side_effect = [
        StubImageStatus(remote_exists=True, local_exists=False),
        StubImageStatus(remote_exists=False, local_exists=True),
    ]

    result = invoke_batch_render(tmp_path, monkeypatch, "8.4", "glibc")

    amqp_image = f"{DEFAULT_IMAGE}:8.4-amqp-glibc"
    redis_image = f"{DEFAULT_IMAGE}:8.4-redis-glibc"
    builder_script = tmp_path / "dst" / "builder-8.4-glibc.sh"
    assert result.exit_code == 0
    assert f"[SKIP] {amqp_image}\n" in result.output
    assert f"[BUILD] {redis_image}\n" in result.output
    assert amqp_image not in builder_script.read_text(encoding="utf-8")
    assert redis_image in builder_script.read_text(encoding="utf-8")
    assert not (tmp_path / "dst" / "8.4" / "glibc" / "amqp.Dockerfile").exists()


@pytest.mark.parametrize("force_option", ["--force", "-f"])
def test_render_batch_force_builds_all_images_without_inspection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    images_are_missing_by_default: Mock,
    force_option: str,
) -> None:
    write_render_inputs(tmp_path)

    result = invoke_batch_render(
        tmp_path,
        monkeypatch,
        force_option,
        "8.4",
        "glibc",
    )

    image = f"{DEFAULT_IMAGE}:8.4-redis-glibc"
    assert result.exit_code == 0
    assert f"[BUILD] {image}\n" in result.output
    images_are_missing_by_default.assert_not_called()


def test_render_batch_writes_no_op_builder_for_empty_modules_directory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    data_directory = tmp_path / "data" / "8.4" / "glibc"
    (data_directory / "modules").mkdir(parents=True)
    (data_directory / "core.Dockerfile").write_text(
        "FROM scratch\n{{ module | raw }}",
        encoding="utf-8",
    )

    result = invoke_batch_render(tmp_path, monkeypatch, "8.4", "glibc")

    builder_script = tmp_path / "dst" / "builder-8.4-glibc.sh"
    assert result.exit_code == 0
    assert builder_script.read_text(encoding="utf-8") == (
        "#!/usr/bin/env bash\nset -euo pipefail\n"
    )
    assert builder_script.stat().st_mode & 0o111
    assert result.output == "Rendered: 0, skipped: 0\n"


def test_render_batch_reports_missing_modules_directory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    data_directory = tmp_path / "data" / "8.4" / "glibc"
    data_directory.mkdir(parents=True)
    (data_directory / "core.Dockerfile").write_text(
        "FROM scratch\n{{ module | raw }}",
        encoding="utf-8",
    )

    result = invoke_batch_render(tmp_path, monkeypatch, "8.4", "glibc")

    assert result.exit_code != 0
    assert f"Module directory not found: {data_directory / 'modules'}" in result.output
    assert not (tmp_path / "dst").exists()


def test_render_batch_reports_missing_core_template_without_writing_outputs(
    tmp_path: Path,
    monkeypatch,
) -> None:
    modules_directory = tmp_path / "data" / "8.4" / "glibc" / "modules"
    modules_directory.mkdir(parents=True)
    (modules_directory / "redis.Dockerfile").write_text(
        "RUN install-redis\n",
        encoding="utf-8",
    )

    result = invoke_batch_render(tmp_path, monkeypatch, "8.4", "glibc")

    core_template = modules_directory.parent / "core.Dockerfile"
    assert result.exit_code != 0
    assert f"Template not found: {core_template}" in result.output
    assert not (tmp_path / "dst").exists()
