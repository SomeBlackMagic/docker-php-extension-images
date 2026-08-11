"""Command-line interface for the Dockerfile renderer."""

import click

from docker_render.builder import (
    build_docker_command,
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
from docker_render.paths import (
    builder_script,
    core_template,
    generated_dockerfile,
    module_file,
    modules_directory,
    repository_root,
)
from docker_render.renderer import render_dockerfile

DEFAULT_IMAGE = "someblackmagic/docker-php-extension-images"


@click.group()
def cli() -> None:
    """Render and build Docker PHP extension images."""


@cli.command("render")
@click.option("--image", default=DEFAULT_IMAGE, show_default=True)
@click.argument("version")
@click.argument("os_variant", metavar="OS")
def render(image: str, version: str, os_variant: str) -> None:
    """Render all extensions for VERSION and OS."""
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
        commands: list[list[str]] = []

        for module_path in module_paths:
            extension = module_path.name.removesuffix(".Dockerfile")
            dockerfile = generated_dockerfile(
                version,
                os_variant,
                extension,
                base_path,
            )
            rendered = render_dockerfile(template_path, module_path)
            dockerfile.parent.mkdir(parents=True, exist_ok=True)
            dockerfile.write_text(rendered, encoding="utf-8")
            commands.append(
                build_docker_command(
                    image=image,
                    version=version,
                    extension=extension,
                    os_variant=os_variant,
                    dockerfile=dockerfile,
                    context=dockerfile.parent,
                    pull=True,
                )
            )

        write_builder_script(
            builder_script(version, os_variant, base_path),
            commands,
        )
        click.echo(
            f"Rendered: {len(module_paths)}, skipped: {len(entries) - len(module_paths)}"
        )
    except DockerRenderError as error:
        raise click.ClickException(str(error)) from error


@cli.command("render-one")
@click.option("--image", default=DEFAULT_IMAGE, show_default=True)
@click.argument("version")
@click.argument("os_variant", metavar="OS")
@click.argument("extension", metavar="EXT")
def render_one(image: str, version: str, os_variant: str, extension: str) -> None:
    """Render and build one extension for VERSION and OS."""
    base_path = repository_root()
    module_path = module_file(version, os_variant, extension, base_path)

    try:
        if not module_path.is_file():
            raise ExtensionNotFound(module_path)

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

        command = build_docker_command(
            image=image,
            version=version,
            extension=extension,
            os_variant=os_variant,
            dockerfile=dockerfile,
            context=dockerfile.parent,
            progress_plain=True,
        )
        run_docker_build(command, verbose=True)
    except DockerBuildError as error:
        click.echo(f"Error: {error}", err=True)
        raise click.exceptions.Exit(error.returncode) from error
    except DockerRenderError as error:
        raise click.ClickException(str(error)) from error


if __name__ == "__main__":
    cli()
