# Module 9: Batch Rendering Workflow

## Goal

Render all valid extension modules for a PHP/OS pair and generate one executable builder script.

## Scope

- Add `render VERSION OS` to the Click CLI.
- Validate the modules directory and core template.
- Select only files ending in `.Dockerfile`.
- Sort modules for deterministic output.
- Render one destination Dockerfile per extension.
- Generate one Docker command per rendered extension.
- Write `dst/builder-<version>-<os>.sh`.
- Report rendered and skipped counts in a stable summary format.

## Deliverables

- Batch `render` implementation in `docker_render/cli.py`
- Batch CLI integration tests

## Acceptance criteria

- Unrelated files such as `.DS_Store` are ignored.
- Output ordering is deterministic.
- Existing builder scripts are replaced atomically enough to avoid stale commands.
- An empty valid modules directory produces a defined, tested result.
- Errors leave an actionable CLI message.

## Dependencies

- Module 4: Template Rendering
- Module 5: Docker Command Construction
- Module 6: Builder Script Generation
- Module 8 establishes the shared CLI error-handling pattern

