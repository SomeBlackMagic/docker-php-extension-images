# Module 13: Registry Build Cache

## Goal

Use a remote BuildKit registry cache to accelerate repeated local and CI builds.

## Scope

- Add `--cache-from type=registry,ref=<ref>` to Buildx commands.
- Add `--cache-to type=registry,ref=<ref>,mode=max` to Buildx commands.
- Generate a default cache reference in the form `<image>:buildcache-<version>-<extension>-<os>`.
- Add `--cache/--no-cache` and `--cache-ref` options to `render` and `render-one`.
- Support `{image}`, `{version}`, `{ext}`, and `{os}` placeholders in a batch cache-reference template.
- Reject the conflicting combination of `--no-cache` and `--cache-ref`.
- Serialize generated shell commands with `shlex.join`.

## Design decisions

Each extension uses a separate cache tag. A shared `:buildcache` tag would allow parallel builds to overwrite the same cache manifest and would mix unrelated dependency graphs.

Remote image existence and build cache availability remain separate concerns. An existing output image may skip a build; an existing cache only accelerates a build that still needs to run.

Docker registry credentials are not CLI inputs. Buildx must use credentials already configured through `docker login` or the CI credential helper.

## Example

```bash
docker buildx build \
  --cache-from type=registry,ref=registry.example.com/app:buildcache-8.1-redis-alpine \
  --cache-to type=registry,ref=registry.example.com/app:buildcache-8.1-redis-alpine,mode=max \
  --push \
  --tag registry.example.com/app:8.1-redis-alpine \
  --file dst/8.1/alpine/redis.Dockerfile \
  dst/8.1/alpine/
```

## Deliverables

- Cache-reference construction in `docker_render/builder.py`
- Cache arguments in Docker command construction
- CLI options and validation in `docker_render/cli.py`
- Unit and CLI integration tests

## Acceptance criteria

- Registry cache import and export are enabled by default in both workflows.
- Every extension receives a deterministic and isolated default cache reference.
- `--no-cache` omits both registry cache arguments.
- A custom cache reference controls both cache import and export.
- Batch placeholder expansion produces a distinct reference per extension.
- Registry credentials never appear in commands, generated scripts, or CLI output.
- Tests require neither a Docker daemon nor registry access.

## Dependencies

- Module 5: Docker Command Construction
- Module 6: Builder Script Generation
- Module 8: Single-Extension Workflow
- Module 9: Batch Rendering Workflow
- Module 10: Existing-Image Detection for consistent build/skip behavior
