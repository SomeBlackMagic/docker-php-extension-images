"""Aggregate verification Dockerfile rendering."""

from collections.abc import Sequence
from pathlib import Path

from jinja2 import TemplateNotFound as JinjaTemplateNotFound

from docker_render.builder import build_image_tag
from docker_render.exceptions import TemplateNotFound
from docker_render.renderer import create_environment


def render_aggregate_dockerfile(
    *,
    template_path: Path,
    image: str,
    version: str,
    os_variant: str,
    extensions: Sequence[str],
) -> str:
    """Render an aggregate Dockerfile for an ordered extension sequence."""
    if not extensions or any(not extension.strip() for extension in extensions):
        raise ValueError("At least one extension is required")

    environment = create_environment(template_path.parent)
    try:
        template = environment.get_template(template_path.name)
    except JinjaTemplateNotFound as error:
        raise TemplateNotFound(template_path) from error

    image_tags = [
        build_image_tag(image, version, extension, os_variant)
        for extension in extensions
    ]
    base_os = "alpine" if os_variant == "musl" else os_variant
    return template.render(
        version=version,
        base_os=base_os,
        image_tags=image_tags,
    )
