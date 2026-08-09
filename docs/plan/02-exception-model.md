# Module 2: Exception Model

## Goal

Define predictable application errors that preserve useful diagnostic information without exposing raw tracebacks during normal CLI use.

## Scope

- Add exceptions for missing data, module directories, extensions, and templates.
- Add `DockerBuildError` with the process return code and stderr.
- Decide which low-level errors are wrapped and which native errors remain visible to the CLI boundary.
- Add unit tests for exception inheritance and message formatting.

## Deliverables

- `docker_render/exceptions.py`
- `tests/test_exceptions.py`

## Acceptance criteria

- Every exception has a meaningful string representation.
- `DockerBuildError` exposes `returncode` and `stderr` as attributes.
- CLI workflows can map application errors to non-zero exit codes without inspecting error strings.

## Dependencies

- Module 1: Project Foundation

