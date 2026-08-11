"""Local and remote Docker image inspection."""

import logging
import subprocess
from dataclasses import dataclass

from docker_render.exceptions import DockerRenderError

REMOTE_MISSING_MESSAGES = (
    "manifest unknown",
    "no such manifest",
)
LOCAL_MISSING_MESSAGES = (
    "no such image",
    "no such object",
)
LOGGER = logging.getLogger(__name__)


class ImageInspectionError(DockerRenderError):
    """Raised when remote image availability cannot be determined."""

    def __init__(self, *, image: str, returncode: int, stderr: str) -> None:
        self.image = image
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(str(self))

    def __str__(self) -> str:
        message = (
            f"Docker image inspection failed for {self.image} "
            f"with exit code {self.returncode}"
        )
        if self.stderr.strip():
            return f"{message}: {self.stderr.strip()}"
        return message


@dataclass(frozen=True)
class ImageStatus:
    """Availability of an image in the registry and local Docker storage."""

    remote_exists: bool
    local_exists: bool | None
    local_error: str | None = None

    @property
    def should_skip(self) -> bool:
        """Return whether a build can be skipped safely."""
        return self.remote_exists


def _contains_any(message: str, candidates: tuple[str, ...]) -> bool:
    normalized = message.casefold()
    return any(candidate in normalized for candidate in candidates)


def check_image_status(image: str) -> ImageStatus:
    """Inspect an image remotely and locally without raising for missing images."""
    LOGGER.info("Checking image availability: %s", image)
    remote_result = subprocess.run(
        ["docker", "manifest", "inspect", image],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )

    if remote_result.returncode == 0:
        remote_exists = True
    elif _contains_any(remote_result.stderr, REMOTE_MISSING_MESSAGES):
        remote_exists = False
    else:
        LOGGER.error("Remote inspection failed for %s", image)
        raise ImageInspectionError(
            image=image,
            returncode=remote_result.returncode,
            stderr=remote_result.stderr,
        )

    local_result = subprocess.run(
        ["docker", "image", "inspect", image],
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )

    if local_result.returncode == 0:
        LOGGER.debug("Image status for %s: remote=%s local=true", image, remote_exists)
        return ImageStatus(remote_exists=remote_exists, local_exists=True)
    if _contains_any(local_result.stderr, LOCAL_MISSING_MESSAGES):
        LOGGER.debug("Image status for %s: remote=%s local=false", image, remote_exists)
        return ImageStatus(remote_exists=remote_exists, local_exists=False)
    LOGGER.warning("Could not determine local image status for %s: %s", image, local_result.stderr.strip() or "unknown error")
    return ImageStatus(
        remote_exists=remote_exists,
        local_exists=None,
        local_error=local_result.stderr.strip() or None,
    )
