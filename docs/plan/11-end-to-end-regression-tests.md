# Module 11: End-to-End Regression Coverage

## Goal

Prove that the Python implementation preserves the required generator behavior across complete CLI workflows.

## Scope

- Create a reusable temporary project-tree fixture.
- Cover rendering multiple modules and one selected module.
- Verify generated Dockerfiles and builder scripts.
- Cover missing data, missing templates, missing extensions, invalid template variables, Docker failures, skip decisions, and forced rebuilds.
- Add coverage reporting and document the standard test command.
- Compare representative generated output with committed expectations or golden files.

## Deliverables

- `tests/conftest.py`
- Cross-module tests in `tests/test_cli.py`
- Golden fixtures where they improve regression clarity
- Documented test command

## Acceptance criteria

- `pytest tests/ -v --cov=docker_render --cov-report=term-missing` succeeds.
- Tests are deterministic and require neither network access nor Docker.
- Both success and failure paths are represented.
- Generated commands preserve multi-platform build behavior.

## Dependencies

- Modules 1 through 10

