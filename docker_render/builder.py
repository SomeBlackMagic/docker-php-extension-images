"""Deterministic Docker Buildx command construction."""

import shlex
import stat
from pathlib import Path

PLATFORMS = "linux/amd64,linux/arm64"


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


def build_image_tag(
    image: str,
    version: str,
    extension: str,
    os_variant: str,
) -> str:
    """Return the image tag shared by build and inspection workflows."""
    return f"{image}:{version}-{extension}-{os_variant}"


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

    return command
