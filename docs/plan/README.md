# Python Rewrite Development Plan

This directory splits the Python rewrite into independently reviewable development modules. Each module should be implemented with its tests in the same change.

## Recommended order

1. [Project foundation](01-project-foundation.md)
2. [Exception model](02-exception-model.md)
3. [Path resolution](03-path-resolution.md)
4. [Template rendering](04-template-rendering.md)
5. [Docker command construction](05-docker-command-construction.md)
6. [Builder script generation](06-builder-script-generation.md)
7. [Docker build execution](07-docker-build-execution.md)
8. [Single-extension workflow](08-render-one-workflow.md)
9. [Batch rendering workflow](09-batch-render-workflow.md)
10. [Existing-image detection](10-image-existence-checking.md)
11. [End-to-end regression coverage](11-end-to-end-regression-tests.md)
12. [Aggregate Dockerfile generation](12-aggregate-dockerfile-generation.md)
13. [Registry build cache](13-registry-build-cache.md)

Modules 2, 3, and 5 can be developed independently after the foundation. Module 12 is required only if `var/Dockerfile` is expected to become generated output of the Python application.
Module 13 can be implemented after Docker command construction and then integrated into both CLI workflows.

## Shared completion rules

- Public behavior is covered by automated tests.
- User-facing failures produce a non-zero exit code and an actionable message.
- Paths are represented by `pathlib.Path`.
- Subprocess commands are represented as argument lists until shell-script serialization is required.
- Existing templates and generated output remain compatible unless a module explicitly documents a migration.
