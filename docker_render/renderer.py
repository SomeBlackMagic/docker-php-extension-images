"""Dockerfile template rendering."""

import logging
from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
)
from jinja2 import (
    TemplateNotFound as JinjaTemplateNotFound,
)

from docker_render.exceptions import TemplateNotFound

LOGGER = logging.getLogger(__name__)


def _raw(value: str) -> str:
    """Preserve the Twig-compatible raw filter used by core templates."""
    return value


def create_environment(template_directory: Path) -> Environment:
    """Create the Jinja environment used for Dockerfile templates."""
    LOGGER.debug("Creating Jinja environment for %s", template_directory)
    environment = Environment(
        loader=FileSystemLoader(template_directory, encoding="utf-8"),
        autoescape=False,
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    environment.filters["raw"] = _raw
    return environment


def render_dockerfile(template_path: Path, module_path: Path) -> str:
    """Render a module fragment into a core Dockerfile template."""
    LOGGER.debug("Rendering template %s with module %s", template_path, module_path)
    environment = create_environment(template_path.parent)

    try:
        template = environment.get_template(template_path.name)
    except JinjaTemplateNotFound as error:
        raise TemplateNotFound(template_path) from error

    module = module_path.read_text(encoding="utf-8")
    rendered = template.render(module=module)
    LOGGER.debug("Rendered Dockerfile (%d bytes)", len(rendered.encode("utf-8")))
    return rendered
