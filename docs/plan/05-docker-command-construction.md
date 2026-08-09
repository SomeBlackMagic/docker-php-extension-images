# Module 5: Docker Command Construction

## Goal

Build deterministic Docker Buildx commands as structured argument lists.

## Scope

- Build commands for `linux/amd64` and `linux/arm64`.
- Include `--push`, image tag, Dockerfile, and context.
- Support optional `--pull` and `--progress plain` behavior.
- Centralize image-tag construction so CLI workflows and image checks use identical tags.
- Keep command construction free of subprocess and file-system side effects.

## Deliverables

- Command-building functions in `docker_render/builder.py`
- Unit tests for tags, flags, ordering, and paths

## Acceptance criteria

- Commands are returned as `list[str]`.
- Batch and single-extension flag combinations are tested.
- The tag format is `<image>:<version>-<extension>-<os>`.
- Context and Dockerfile paths are passed as individual arguments.

## Dependencies

- Module 1: Project Foundation
- Module 3: Path Resolution

