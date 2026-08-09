# Module 12: Aggregate Dockerfile Generation

## Goal

Generate the aggregate verification image represented by `var/Dockerfile`, if that file is intended to be managed by the rewritten application.

## Reference behavior

The current file:

- Starts from a PHP version and OS-specific base image.
- Installs common build tools.
- Copies files from multiple extension images with `COPY --from`.
- Uses tags in the form `<image>:<version>-<extension>-<os>`.
- Runs PHP version and startup-error checks.
- Removes the temporary `php.ini` after verification.

## Scope

- Define whether aggregate extension order is configuration-driven or derived from module discovery.
- Add a dedicated aggregate Dockerfile template.
- Reuse the centralized image-tag builder.
- Render deterministic `COPY --from` instructions.
- Preserve the verification commands from `var/Dockerfile`.
- Define the output path and expose generation through the appropriate CLI workflow.
- Add regression coverage against the current PHP 7.4 Alpine example.

## Deliverables

- Aggregate Dockerfile template
- Aggregate rendering function or dedicated renderer module
- Path and CLI integration
- Tests and a representative expected Dockerfile

## Acceptance criteria

- PHP version, OS, image repository, and extensions are configurable inputs.
- Generated extension tags exactly match the individual build tags.
- Extension ordering is deterministic.
- The generated PHP 7.4 Alpine result is behaviorally equivalent to `var/Dockerfile`.
- Missing or empty extension input is rejected with a clear error.

## Dependencies

- Module 3: Path Resolution
- Module 4: Template Rendering
- Module 5: Docker Command Construction
- Module 9: Batch Rendering Workflow
- Module 11: End-to-End Regression Coverage patterns

## Open decision

Confirm whether `var/Dockerfile` is generated output or a manually maintained example. If it remains manual, this module can be omitted and the rewrite contains 11 development modules.
