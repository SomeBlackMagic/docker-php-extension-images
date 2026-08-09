# Module 10: Existing-Image Detection

## Goal

Avoid rebuilding images already published in the registry while allowing explicit forced rebuilds.

## Scope

- Add remote inspection using `docker manifest inspect`.
- Optionally report local status using `docker image inspect` for diagnostics.
- Add an `ImageStatus` value object.
- Add `--force` / `-f` to both CLI workflows.
- Use one consistent skip rule in both commands.
- Report `[SKIP]` and `[BUILD]` decisions in batch mode.

## Decision

Remote existence is the authoritative skip condition because builds use `--push`. Local existence alone must not skip a build. `--force` bypasses all existence checks.

## Deliverables

- `docker_render/image_checker.py`
- `tests/test_image_checker.py`
- CLI integration for both workflows

## Acceptance criteria

- A remotely existing image is skipped consistently by `render` and `render-one`.
- A locally existing but remotely missing image is built.
- `--force` builds without invoking existence checks.
- Inspection failures are distinguishable from a confirmed missing manifest where practical.
- Tests do not access a real registry or Docker daemon.

## Dependencies

- Module 5: Docker Command Construction
- Module 8: Single-Extension Workflow
- Module 9: Batch Rendering Workflow

