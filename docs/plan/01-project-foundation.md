# Module 1: Project Foundation

## Goal

Create an installable Python 3.11+ project with a stable CLI entry point and a test environment.

## Scope

- Add `pyproject.toml` with project metadata.
- Add runtime dependencies on Click and Jinja2.
- Add pytest and pytest-cov as development dependencies.
- Create the `docker_render` package and its `__init__.py`.
- Register `render = "docker_render.cli:cli"` as a console script.
- Add the root `render` compatibility launcher if direct repository execution is required.
- Create a minimal Click command group and a test proving it starts.

## Deliverables

- `pyproject.toml`
- `docker_render/__init__.py`
- `docker_render/cli.py`
- `render`
- Initial CLI smoke test

## Acceptance criteria

- `pip install -e ".[dev]"` succeeds.
- `render --help` exits with code 0.
- `python render --help` exits with code 0 when the compatibility launcher is included.
- `pytest` discovers and runs the smoke test.

## Dependencies

None.

