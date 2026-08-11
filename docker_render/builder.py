"""Deterministic Docker Buildx command construction."""

import logging
import shlex
import stat
from pathlib import Path
from string import Formatter

PLATFORMS = "linux/amd64,linux/arm64"
LOGGER = logging.getLogger(__name__)


def write_builder_script(destination: Path, commands: list[list[str]]) -> None:
    """Write commands as an executable Bash script."""
    lines = [
        "#!/usr/bin/env bash",
        "set -euo pipefail",
        *(shlex.join(command) for command in commands),
    ]
    content = "\n".join(lines) + "\n"

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")

    executable_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    destination.chmod(destination.stat().st_mode | executable_bits)
    LOGGER.info("Wrote executable builder script %s with %d commands", destination, len(commands))


def build_image_tag(
    image: str,
    version: str,
    extension: str,
    os_variant: str,
) -> str:
    """Return the image tag shared by build and inspection workflows."""
    return f"{image}:{version}-{extension}-{os_variant}"


def build_cache_reference(
    image: str,
    version: str,
    extension: str,
    os_variant: str,
) -> str:
    """Return the isolated default registry cache reference for an extension."""
    return f"{image}:buildcache-{version}-{extension}-{os_variant}"


def expand_cache_reference_template(
    template: str,
    *,
    image: str,
    version: str,
    extension: str,
    os_variant: str,
) -> str:
    """Expand the supported placeholders in a batch cache reference template."""
    values = {
        "image": image,
        "version": version,
        "ext": extension,
        "os": os_variant,
    }

    try:
        fields = [
            field_name
            for _, field_name, _, _ in Formatter().parse(template)
            if field_name is not None
        ]
    except ValueError as error:
        raise ValueError(f"Invalid cache reference template: {error}") from error

    for field_name in fields:
        if field_name not in values:
            raise ValueError(f"Unknown cache reference placeholder: {field_name}")

    return template.format_map(values)


def build_docker_command(
    *,
    image: str,
    version: str,
    extension: str,
    os_variant: str,
    dockerfile: Path,
    context: Path,
    pull: bool = False,
    progress_plain: bool = False,
    cache: bool = True,
    cache_ref: str | None = None,
) -> list[str]:
    """Return a structured Docker Buildx command without side effects."""
    command = [
        "docker",
        "buildx",
        "build",
        "--platform",
        PLATFORMS,
    ]

    if progress_plain:
        command.extend(["--progress", "plain"])

    if cache:
        resolved_cache_ref = cache_ref or build_cache_reference(
            image,
            version,
            extension,
            os_variant,
        )
        command.extend(
            [
                "--cache-from",
                f"type=registry,ref={resolved_cache_ref}",
                "--cache-to",
                f"type=registry,ref={resolved_cache_ref},mode=max",
            ]
        )

    command.append("--push")

    if pull:
        command.append("--pull")

    command.extend(
        [
            "--tag",
            build_image_tag(image, version, extension, os_variant),
            "--file",
            str(dockerfile),
            str(context),
        ]
    )

    LOGGER.debug("Constructed Docker command: %s", shlex.join(command))
    return command
