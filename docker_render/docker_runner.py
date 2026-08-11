"""Docker subprocess execution."""

import subprocess

from docker_render.exceptions import DockerBuildError


def run_docker_build(command: list[str], *, verbose: bool = False) -> None:
    """Run a Docker build command and raise a typed error on failure."""
    result = subprocess.run(
        command,
        check=False,
        capture_output=not verbose,
        text=True,
        shell=False,
    )

    if result.returncode != 0:
        raise DockerBuildError(
            returncode=result.returncode,
            stderr=result.stderr or "",
        )
