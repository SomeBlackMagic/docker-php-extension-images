"""Tests for Dockerfile template rendering."""

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

import pytest
from jinja2 import UndefinedError

from docker_render.exceptions import TemplateNotFound

RENDERER_MODULE_NAME = "docker_render.renderer"
RENDERER_MODULE_EXISTS = find_spec(RENDERER_MODULE_NAME) is not None


def test_renderer_module_exists() -> None:
    assert RENDERER_MODULE_EXISTS


@pytest.fixture
def renderer() -> ModuleType:
    if not RENDERER_MODULE_EXISTS:
        pytest.skip(f"{RENDERER_MODULE_NAME} is not implemented yet")

    return import_module(RENDERER_MODULE_NAME)


def write_render_inputs(
    tmp_path: Path,
    *,
    template: str,
    module: str,
) -> tuple[Path, Path]:
    template_path = tmp_path / "core.Dockerfile"
    module_path = tmp_path / "modules" / "example.Dockerfile"
    module_path.parent.mkdir()
    template_path.write_text(template, encoding="utf-8")
    module_path.write_text(module, encoding="utf-8")
    return template_path, module_path


def test_renders_module_without_html_escaping(
    renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path, module_path = write_render_inputs(
        tmp_path,
        template="before\n{{ module | raw }}\nafter\n",
        module="RUN printf '<tag attr=\"value\"> & content'\n",
    )

    rendered = renderer.render_dockerfile(template_path, module_path)

    assert rendered == (
        "before\nRUN printf '<tag attr=\"value\"> & content'\n\nafter\n"
    )


def test_undefined_template_variable_fails_explicitly(
    renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path, module_path = write_render_inputs(
        tmp_path,
        template="{{ missing_variable }}\n",
        module="RUN true\n",
    )

    with pytest.raises(UndefinedError, match="missing_variable"):
        renderer.render_dockerfile(template_path, module_path)


def test_missing_template_raises_application_error(
    renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path = tmp_path / "missing-core.Dockerfile"
    module_path = tmp_path / "example.Dockerfile"
    module_path.write_text("RUN true\n", encoding="utf-8")

    with pytest.raises(TemplateNotFound) as error_info:
        renderer.render_dockerfile(template_path, module_path)

    assert error_info.value.path == template_path
    assert str(error_info.value) == f"Template not found: {template_path}"
    assert error_info.value.__cause__ is not None


def test_reads_module_content_as_utf_8(
    renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path, module_path = write_render_inputs(
        tmp_path,
        template="{{ module | raw }}",
        module="RUN printf 'Grüße — 你好'\n",
    )

    rendered = renderer.render_dockerfile(template_path, module_path)

    assert rendered == "RUN printf 'Grüße — 你好'\n"


@pytest.mark.parametrize(
    ("template", "expected"),
    [
        ("FROM scratch\n{{ module | raw }}\n", "FROM scratch\nRUN true\n\n"),
        ("FROM scratch\n{{ module | raw }}", "FROM scratch\nRUN true\n"),
    ],
)
def test_preserves_template_trailing_newline(
    renderer: ModuleType,
    tmp_path: Path,
    template: str,
    expected: str,
) -> None:
    template_path, module_path = write_render_inputs(
        tmp_path,
        template=template,
        module="RUN true\n",
    )

    assert renderer.render_dockerfile(template_path, module_path) == expected
