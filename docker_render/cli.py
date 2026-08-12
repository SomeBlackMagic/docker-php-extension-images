"""Command-line interface for the Dockerfile renderer."""

import logging

import click

from docker_render.aggregate_renderer import render_aggregate_dockerfile
from docker_render.builder import (
    build_docker_command,
    build_image_tag,
    expand_cache_reference_template,
    write_builder_script,
)
from docker_render.docker_runner import run_docker_build
from docker_render.exceptions import (
    DockerBuildError,
    DockerRenderError,
    ExtensionNotFound,
    ModuleDirectoryNotFound,
    TemplateNotFound,
)
from docker_render.image_checker import check_image_status
from docker_render.paths import (
    aggregate_dockerfile,
    aggregate_template,
    builder_script,
    core_template,
    generated_dockerfile,
    module_file,
    modules_directory,
    repository_root,
)
from docker_render.renderer import render_dockerfile

DEFAULT_IMAGE = "someblackmagic/docker-php-extension-images"
LOGGER = logging.getLogger(__name__)


def _configure_logging(verbosity: int) -> None:
    """Configure application logging from the repeatable CLI verbosity flag."""
    level = logging.DEBUG if verbosity > 1 else logging.INFO if verbosity else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        force=True,
    )


@click.group()
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Show progress logs; repeat for detailed diagnostics.",
)
def cli(verbose: int) -> None:
    """Render and build Docker PHP extension images."""
    _configure_logging(verbose)
    LOGGER.debug("Logging initialized (verbosity=%d)", verbose)


@cli.command("aggregate")
@click.option("--image", default=DEFAULT_IMAGE, show_default=True)
@click.argument("version")
@click.argument("os_variant", metavar="OS")
@click.argument("extensions", metavar="EXTENSIONS...", nargs=-1, required=True)
def aggregate(
    image: str,
    version: str,
    os_variant: str,
    extensions: tuple[str, ...],
) -> None:
    """Render an aggregate verification Dockerfile."""
    LOGGER.info(
        "Rendering aggregate Dockerfile: image=%s version=%s os=%s extensions=%s",
        image,
        version,
        os_variant,
        ",".join(extensions),
    )
    base_path = repository_root()
    destination = aggregate_dockerfile(base_path)

    try:
        rendered = render_aggregate_dockerfile(
            template_path=aggregate_template(base_path),
            image=image,
            version=version,
            os_variant=os_variant,
            extensions=extensions,
        )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rendered, encoding="utf-8")
        LOGGER.info("Wrote aggregate Dockerfile to %s", destination)
        click.echo(f"Rendered aggregate Dockerfile: {destination}")
    except DockerRenderError as error:
        raise click.ClickException(str(error)) from error


@cli.command("render")
@click.option("--image", default=DEFAULT_IMAGE, show_default=True)
@click.option("--cache/--no-cache", default=True, show_default=True)
@click.option("--cache-ref")
@click.option("--force", "-f", is_flag=True, default=False, help="Force rebuilds.")
@click.argument("version")
@click.argument("os_variant", metavar="OS")
def render(
    image: str,
    cache: bool,
    cache_ref: str | None,
    force: bool,
    version: str,
    os_variant: str,
) -> None:
    """Render all extensions for VERSION and OS."""
    LOGGER.info(
        "Starting batch render: image=%s version=%s os=%s cache=%s force=%s",
        image,
        version,
        os_variant,
        cache,
        force,
    )
    if not cache and cache_ref is not None:
        raise click.ClickException("--no-cache cannot be used with --cache-ref")

    if cache_ref is not None:
        try:
            expand_cache_reference_template(
                cache_ref,
                image=image,
                version=version,
                extension="",
                os_variant=os_variant,
            )
        except ValueError as error:
            raise click.ClickException(str(error)) from error

    base_path = repository_root()
    modules_path = modules_directory(version, os_variant, base_path)
    template_path = core_template(version, os_variant, base_path)

    try:
        if not modules_path.is_dir():
            raise ModuleDirectoryNotFound(modules_path)
        if not template_path.is_file():
            raise TemplateNotFound(template_path)

        entries = list(modules_path.iterdir())
        module_paths = sorted(
            (
                path
                for path in entries
                if path.is_file() and path.name.endswith(".Dockerfile")
            ),
            key=lambda path: path.name,
        )
        LOGGER.info("Found %d extension modules in %s", len(module_paths), modules_path)
        commands: list[list[str]] = []
        image_skips = 0

        for module_path in module_paths:
            extension = module_path.name.removesuffix(".Dockerfile")
            image_tag = build_image_tag(image, version, extension, os_variant)
            LOGGER.info("Processing extension %s", extension)
            if force:
                click.echo(f"[BUILD] {image_tag}")
            else:
                image_status = check_image_status(image_tag)
                LOGGER.debug(
                    "Image status for %s: remote=%s local=%s local_error=%s",
                    image_tag,
                    image_status.remote_exists,
                    image_status.local_exists,
                    image_status.local_error,
                )
                if image_status.should_skip:
                    click.echo(f"[SKIP] {image_tag}")
                    image_skips += 1
                    continue
                if image_status.local_exists:
                    click.echo(f"[BUILD] {image_tag}")

            resolved_cache_ref = (
                expand_cache_reference_template(
                    cache_ref,
                    image=image,
                    version=version,
                    extension=extension,
                    os_variant=os_variant,
                )
                if cache_ref is not None
                else None
            )
            dockerfile = generated_dockerfile(
                version,
                os_variant,
                extension,
                base_path,
            )
            rendered = render_dockerfile(template_path, module_path)
            dockerfile.parent.mkdir(parents=True, exist_ok=True)
            dockerfile.write_text(rendered, encoding="utf-8")
            LOGGER.info("Wrote Dockerfile for %s to %s", extension, dockerfile)
            commands.append(
                build_docker_command(
                    image=image,
                    version=version,
                    extension=extension,
                    os_variant=os_variant,
                    dockerfile=dockerfile,
                    context=dockerfile.parent,
                    pull=True,
                    cache=cache,
                    cache_ref=resolved_cache_ref,
                )
            )

        write_builder_script(
            builder_script(version, os_variant, base_path),
            commands,
        )
        LOGGER.info("Batch render completed: rendered=%d skipped=%d", len(commands), len(entries) - len(module_paths) + image_skips)
        click.echo(
            f"Rendered: {len(commands)}, "
            f"skipped: {len(entries) - len(module_paths) + image_skips}"
        )
    except DockerRenderError as error:
        raise click.ClickException(str(error)) from error


@cli.command("render-one")
@click.option("--image", default=DEFAULT_IMAGE, show_default=True)
@click.option("--cache/--no-cache", default=True, show_default=True)
@click.option("--cache-ref")
@click.option("--force", "-f", is_flag=True, default=False, help="Force rebuild.")
@click.argument("version")
@click.argument("os_variant", metavar="OS")
@click.argument("extension", metavar="EXT")
def render_one(
    image: str,
    cache: bool,
    cache_ref: str | None,
    force: bool,
    version: str,
    os_variant: str,
    extension: str,
) -> None:
    """Render and build one extension for VERSION and OS."""
    LOGGER.info(
        "Starting single build: image=%s version=%s os=%s extension=%s cache=%s force=%s",
        image,
        version,
        os_variant,
        extension,
        cache,
        force,
    )
    if not cache and cache_ref is not None:
        raise click.ClickException("--no-cache cannot be used with --cache-ref")

    base_path = repository_root()
    module_path = module_file(version, os_variant, extension, base_path)

    try:
        if not module_path.is_file():
            raise ExtensionNotFound(module_path)

        image_tag = build_image_tag(image, version, extension, os_variant)
        if force:
            click.echo(f"[BUILD] {image_tag}")
        else:
            image_status = check_image_status(image_tag)
            LOGGER.debug(
                "Image status for %s: remote=%s local=%s local_error=%s",
                image_tag,
                image_status.remote_exists,
                image_status.local_exists,
                image_status.local_error,
            )
            if image_status.should_skip:
                click.echo(f"[SKIP] {image_tag}")
                return
            if image_status.local_exists:
                click.echo(f"[BUILD] {image_tag}")

        dockerfile = generated_dockerfile(
            version,
            os_variant,
            extension,
            base_path,
        )
        rendered = render_dockerfile(
            core_template(version, os_variant, base_path),
            module_path,
        )
        dockerfile.parent.mkdir(parents=True, exist_ok=True)
        dockerfile.write_text(rendered, encoding="utf-8")
        LOGGER.info("Wrote Dockerfile to %s", dockerfile)

        resolved_cache_ref = (
            expand_cache_reference_template(
                cache_ref,
                image=image,
                version=version,
                extension=extension,
                os_variant=os_variant,
            )
            if cache_ref is not None
            else None
        )
        command = build_docker_command(
            image=image,
            version=version,
            extension=extension,
            os_variant=os_variant,
            dockerfile=dockerfile,
            context=dockerfile.parent,
            progress_plain=True,
            cache=cache,
            cache_ref=resolved_cache_ref,
        )
        LOGGER.info("Starting Docker build for %s", image_tag)
        run_docker_build(command, verbose=True)
        LOGGER.info("Docker build completed for %s", image_tag)
    except DockerBuildError as error:
        click.echo(f"Error: {error}", err=True)
        raise click.exceptions.Exit(error.returncode) from error
    except DockerRenderError as error:
        raise click.ClickException(str(error)) from error


if __name__ == "__main__":
    cli()
