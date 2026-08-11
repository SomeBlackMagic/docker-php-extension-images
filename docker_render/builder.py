"""Deterministic Docker Buildx command construction."""

from pathlib import Path

PLATFORMS = "linux/amd64,linux/arm64"


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
