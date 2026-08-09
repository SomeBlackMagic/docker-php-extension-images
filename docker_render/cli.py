"""Command-line interface for the Dockerfile renderer."""

import click


@click.group()
def cli() -> None:
    """Render and build Docker PHP extension images."""


if __name__ == "__main__":
    cli()

