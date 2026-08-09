# Module 3: Path Resolution

## Goal

Make `paths.py` the single source of truth for repository input and output locations.

## Scope

- Resolve the repository base path from the installed package location.
- Provide functions for data directories, module directories, module files, core templates, destination directories, generated Dockerfiles, and builder scripts.
- Accept an optional base path so tests can use `tmp_path` without monkeypatching global state.
- Avoid string concatenation and duplicate path separators.

## Deliverables

- `docker_render/paths.py`
- `tests/test_paths.py`

## Acceptance criteria

- Every path used by later modules is produced by a named path function.
- Tests cover multiple PHP versions, OS variants, and extension names.
- Returned values are `Path` instances.
- No function creates directories or performs other I/O.

## Dependencies

- Module 1: Project Foundation

