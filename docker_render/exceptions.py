"""Application-specific exceptions for the Docker PHP extension image renderer."""

from __future__ import annotations

from pathlib import Path


class DockerRenderError(Exception):
    """Base class for all docker-render errors."""


class _PathError(DockerRenderError):
    """Mixin for errors that are tied to a filesystem path."""

    _message_prefix: str

    def __init__(self, path: Path) -> None:
        self.path = path
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"{self._message_prefix}: {self.path}"


class DataDirectoryNotFound(_PathError):
    _message_prefix = "Data directory not found"


class ModuleDirectoryNotFound(_PathError):
    _message_prefix = "Module directory not found"


class ExtensionNotFound(_PathError):
    _message_prefix = "Extension file not found"


class TemplateNotFound(_PathError):
    _message_prefix = "Template not found"


class DockerBuildError(DockerRenderError):
    """Raised when a ``docker build`` subprocess exits with a non-zero status."""

    def __init__(self, *, returncode: int, stderr: str) -> None:
        self.returncode = returncode
        self.stderr = stderr
        super().__init__(str(self))

    def __str__(self) -> str:
        message = f"Docker build failed with exit code {self.returncode}"
        stripped = self.stderr.strip()
        if stripped:
            message = f"{message}: {stripped}"
        return message
