# Module 6: Builder Script Generation

## Goal

Serialize Docker commands into a reliable executable Bash script for batch builds.

## Scope

- Create the destination directory when necessary.
- Write the complete script in one file operation.
- Add a Bash shebang and strict execution options.
- Serialize argument lists with `shlex.join` so spaces and shell metacharacters are quoted safely.
- Mark the generated script executable.
- Define behavior for an empty command list.

## Deliverables

- Script-writing functionality in `docker_render/builder.py`
- Builder script tests

## Acceptance criteria

- The generated file is executable.
- Arguments containing spaces or shell metacharacters round-trip safely.
- Re-running generation replaces stale content instead of appending to it.
- Parent directories are created automatically.

## Dependencies

- Module 5: Docker Command Construction

