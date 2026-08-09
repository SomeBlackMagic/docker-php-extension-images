# Module 8: Single-Extension Workflow

## Goal

Provide `render-one` as the first complete vertical workflow: validate one extension, render its Dockerfile, and build it.

## Scope

- Add `render-one VERSION OS EXT` to the Click CLI.
- Support the configurable image repository option.
- Validate the exact module file rather than only its parent directory.
- Create the destination directory.
- Render and write the extension Dockerfile as UTF-8.
- Build with plain progress and without the batch-only pull option.
- Map application errors and Docker failures to clear CLI output and exit codes.

## Deliverables

- `render-one` implementation in `docker_render/cli.py`
- Focused CLI integration tests

## Acceptance criteria

- A valid module produces the expected Dockerfile and invokes the expected Docker command once.
- A missing extension exits non-zero and identifies the missing extension.
- Docker's non-zero return code is preserved by the command.
- Tests use Click's `CliRunner` and a mocked Docker runner.

## Dependencies

- Modules 2 through 5
- Module 7: Docker Build Execution

