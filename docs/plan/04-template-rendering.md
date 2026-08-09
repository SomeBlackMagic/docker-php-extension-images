# Module 4: Template Rendering

## Goal

Render extension Dockerfiles from the existing `core.Dockerfile` templates without changing their compatible Jinja/Twig placeholder syntax.

## Scope

- Create a Jinja2 environment with file-system loading.
- Disable HTML escaping because the output is a Dockerfile.
- Enable `StrictUndefined` and preserve trailing newlines.
- Load module fragments as UTF-8.
- Render the `module` value into `core.Dockerfile`.
- Translate missing-template failures into the application exception model.

## Deliverables

- `docker_render/renderer.py`
- `tests/test_renderer.py`

## Acceptance criteria

- Module content is inserted without HTML escaping.
- Undefined template variables fail explicitly.
- Missing templates produce a meaningful application error.
- The rendered output preserves the expected final newline.

## Dependencies

- Module 2: Exception Model
- Module 3: Path Resolution

