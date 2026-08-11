"""Tests for aggregate verification Dockerfile rendering."""

from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
from types import ModuleType

import pytest

from docker_render.exceptions import TemplateNotFound

AGGREGATE_RENDERER_MODULE_NAME = "docker_render.aggregate_renderer"
AGGREGATE_RENDERER_MODULE_EXISTS = find_spec(AGGREGATE_RENDERER_MODULE_NAME) is not None
EXTENSIONS = (
    "mysqli",
    "pdo_mysql",
    "propro",
    "raphf",
    "redis",
    "sockets",
    "zip",
    "http",
)


def test_aggregate_renderer_module_exists() -> None:
    assert AGGREGATE_RENDERER_MODULE_EXISTS


@pytest.fixture
def aggregate_renderer() -> ModuleType:
    if not AGGREGATE_RENDERER_MODULE_EXISTS:
        pytest.skip(f"{AGGREGATE_RENDERER_MODULE_NAME} is not implemented yet")

    return import_module(AGGREGATE_RENDERER_MODULE_NAME)


def test_renders_php_7_4_musl_golden_file(
    aggregate_renderer: ModuleType,
) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    expected_path = (
        repository_root / "tests" / "fixtures" / "aggregate" / "php-7.4-musl.Dockerfile"
    )

    rendered = aggregate_renderer.render_aggregate_dockerfile(
        template_path=repository_root / "templates" / "aggregate.Dockerfile",
        image="someblackmagic/docker-php-extension-images",
        version="7.4",
        os_variant="musl",
        extensions=EXTENSIONS,
    )

    assert rendered == expected_path.read_text(encoding="utf-8")


def test_preserves_configured_extension_order_and_uses_shared_tags(
    aggregate_renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path = tmp_path / "aggregate.Dockerfile"
    template_path.write_text(
        "{% for image_tag in image_tags %}COPY --from={{ image_tag }} / /\n{% endfor %}",
        encoding="utf-8",
    )

    rendered = aggregate_renderer.render_aggregate_dockerfile(
        template_path=template_path,
        image="registry.example.com/php-extensions",
        version="8.4",
        os_variant="custom-linux",
        extensions=("redis", "amqp"),
    )

    assert rendered == (
        "COPY --from=registry.example.com/php-extensions:8.4-redis-custom-linux / /\n"
        "COPY --from=registry.example.com/php-extensions:8.4-amqp-custom-linux / /\n"
    )


def test_rejects_empty_extensions(
    aggregate_renderer: ModuleType, tmp_path: Path
) -> None:
    template_path = tmp_path / "aggregate.Dockerfile"
    template_path.write_text("FROM scratch\n", encoding="utf-8")

    with pytest.raises(ValueError, match="At least one extension is required"):
        aggregate_renderer.render_aggregate_dockerfile(
            template_path=template_path,
            image="example/php-extensions",
            version="8.4",
            os_variant="musl",
            extensions=(),
        )


@pytest.mark.parametrize("extension", ["", "   "])
def test_rejects_empty_extension_name(
    aggregate_renderer: ModuleType,
    tmp_path: Path,
    extension: str,
) -> None:
    template_path = tmp_path / "aggregate.Dockerfile"
    template_path.write_text("FROM scratch\n", encoding="utf-8")

    with pytest.raises(ValueError, match="At least one extension is required"):
        aggregate_renderer.render_aggregate_dockerfile(
            template_path=template_path,
            image="example/php-extensions",
            version="8.4",
            os_variant="musl",
            extensions=(extension,),
        )


def test_missing_template_raises_application_error(
    aggregate_renderer: ModuleType,
    tmp_path: Path,
) -> None:
    template_path = tmp_path / "missing-aggregate.Dockerfile"

    with pytest.raises(TemplateNotFound) as error_info:
        aggregate_renderer.render_aggregate_dockerfile(
            template_path=template_path,
            image="example/php-extensions",
            version="8.4",
            os_variant="musl",
            extensions=("redis",),
        )

    assert error_info.value.path == template_path
