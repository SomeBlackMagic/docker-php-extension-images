# Module 7: Docker Build Execution

## Goal

Execute a structured Docker command and report failures through a typed error.

## Scope

- Run Docker through `subprocess.run` without invoking a shell.
- Capture stdout and stderr in non-verbose mode.
- Stream output directly in verbose mode.
- Raise `DockerBuildError` for non-zero return codes.
- Preserve the Docker process exit code for the CLI.

## Deliverables

- `docker_render/docker_runner.py`
- `tests/test_docker_runner.py`

## Acceptance criteria

- A successful process returns normally.
- A failed process raises `DockerBuildError` with the original exit code.
- Verbose mode does not capture output.
- Tests mock subprocess execution and never require a Docker daemon.

## Dependencies

- Module 2: Exception Model

