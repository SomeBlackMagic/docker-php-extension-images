"""Docker subprocess execution."""

import logging
import shlex
import subprocess

from docker_render.exceptions import DockerBuildError

LOGGER = logging.getLogger(__name__)


def run_docker_build(command: list[str], *, verbose: bool = False) -> None:
    """Run a Docker build command and raise a typed error on failure."""
    LOGGER.info("Running Docker build")
    LOGGER.debug("Executing: %s", shlex.join(command))
    result = subprocess.run(
        command,
        check=False,
        capture_output=not verbose,
        text=True,
        shell=False,
    )

    if result.returncode != 0:
        LOGGER.error("Docker build failed with exit code %d", result.returncode)
        raise DockerBuildError(
            returncode=result.returncode,
            stderr=result.stderr or "",
        )
    LOGGER.info("Docker build process finished successfully")
