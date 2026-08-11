"""Repository path resolution."""

from pathlib import Path


def repository_root(base_path: Path | None = None) -> Path:
    """Return the repository root or an explicitly supplied base path."""
    if base_path is not None:
        return base_path

    return Path(__file__).resolve().parents[1]


def data_directory(
    version: str,
    os_variant: str,
    base_path: Path | None = None,
) -> Path:
    """Return the data directory for a PHP version and OS variant."""
    return repository_root(base_path) / "data" / version / os_variant


def modules_directory(
    version: str,
    os_variant: str,
    base_path: Path | None = None,
) -> Path:
    """Return the extension module directory."""
    return data_directory(version, os_variant, base_path) / "modules"


def module_file(
    version: str,
    os_variant: str,
    extension: str,
    base_path: Path | None = None,
) -> Path:
    """Return the source Dockerfile fragment for an extension."""
    return modules_directory(version, os_variant, base_path) / f"{extension}.Dockerfile"


def core_template(
    version: str,
    os_variant: str,
    base_path: Path | None = None,
) -> Path:
    """Return the core Dockerfile template."""
    return data_directory(version, os_variant, base_path) / "core.Dockerfile"


def destination_directory(
    version: str,
    os_variant: str,
    base_path: Path | None = None,
) -> Path:
    """Return the generated Dockerfile directory."""
    return repository_root(base_path) / "dst" / version / os_variant


def generated_dockerfile(
    version: str,
    os_variant: str,
    extension: str,
    base_path: Path | None = None,
) -> Path:
    """Return the generated Dockerfile path for an extension."""
    return destination_directory(version, os_variant, base_path) / (
        f"{extension}.Dockerfile"
    )


def builder_script(
    version: str,
    os_variant: str,
    base_path: Path | None = None,
) -> Path:
    """Return the generated batch builder script path."""
    return repository_root(base_path) / "dst" / f"builder-{version}-{os_variant}.sh"
