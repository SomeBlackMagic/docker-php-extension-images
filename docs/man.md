# Rendering and Building Images

Run all commands from the repository root. The current renderer is written in
Python and is executed with `uv`. The `php bin/console render` commands in
`docs/SetupRunners.md` belong to an older version of the project.

## Prerequisites

Install the project dependencies:

```bash
uv sync
```

Docker is not required to render Dockerfiles. Building and publishing images
requires Docker Buildx, a configured builder (see `docs/SetupRunners.md`), and
authentication with the destination registry:

```bash
docker buildx use local_remote_builder
docker buildx inspect --bootstrap
docker login
```

Inspect the available commands and arguments with:

```bash
uv run render --help
uv run render render --help
uv run render render-one --help
uv run render aggregate --help
```

The repository contains PHP versions `7.4`, `8.0`, `8.1`, `8.2`, `8.3`, `8.4`,
and `8.5`. Each version has `glibc` and `musl` variants.

## Render All Extensions

The command syntax is:

```bash
uv run render render [--image IMAGE] [--cache | --no-cache] \
  [--cache-ref CACHE_REF] [--force] VERSION OS
```

For example:

```bash
uv run render render 8.4 glibc
uv run render render 8.4 musl
```

The command reads `data/<version>/<os>/core.Dockerfile` and all Dockerfile
fragments in `data/<version>/<os>/modules/`. It creates:

- rendered Dockerfiles in `dst/<version>/<os>/`;
- an executable `dst/builder-<version>-<os>.sh` script.

Rendering does not build or publish images. Execute the generated scripts to
start the builds:

```bash
./dst/builder-8.4-glibc.sh
./dst/builder-8.4-musl.sh
```

Every generated Buildx command builds `linux/amd64` and `linux/arm64` and uses
`--push` to publish the result. The default image repository is
`someblackmagic/docker-php-extension-images`. Select another repository while
rendering with `--image`:

```bash
uv run render render \
  --image registry.example.com/team/php-extensions \
  8.4 musl

./dst/builder-8.4-musl.sh
```

Rendering the same version and OS again replaces the corresponding Dockerfiles
and builder script.

## Render the Complete Matrix

Render all supported PHP and OS combinations:

```bash
for version in 7.4 8.0 8.1 8.2 8.3 8.4 8.5; do
  for os in glibc musl; do
    uv run render render "$version" "$os"
  done
done
```

After reviewing the generated files, build the complete matrix:

```bash
for version in 7.4 8.0 8.1 8.2 8.3 8.4 8.5; do
  for os in glibc musl; do
    "./dst/builder-${version}-${os}.sh"
  done
done
```

The scripts use `set -euo pipefail`, so the loop stops at the first failed
build.

## Render and Build One Extension

The command syntax is:

```bash
uv run render render-one [--image IMAGE] [--cache | --no-cache] \
  [--cache-ref CACHE_REF] [--force] VERSION OS EXTENSION
```

For example:

```bash
uv run render render-one 8.4 musl redis
```

This command creates `dst/8.4/musl/redis.Dockerfile`, immediately starts a
Buildx build for `linux/amd64,linux/arm64`, and publishes the image as
`someblackmagic/docker-php-extension-images:8.4-redis-musl`. Unlike the batch
`render` command, `render-one` does not create a builder script.

The source extension must exist at
`data/<version>/<os>/modules/<extension>.Dockerfile`.

## Build Cache

Registry cache is enabled by default for both `render` and `render-one`. You do
not need to specify anything to use it. For example:

```bash
uv run render render-one 8.4 musl redis
```

This publishes the final image and its cache to the default Docker Hub
repository using different tags:

```text
Final image:
someblackmagic/docker-php-extension-images:8.4-redis-musl

Cache:
someblackmagic/docker-php-extension-images:buildcache-8.4-redis-musl
```

The CLI adds both of these Buildx options automatically:

```text
--cache-from type=registry,ref=<cache reference>
--cache-to type=registry,ref=<cache reference>,mode=max
```

The first build creates the cache. Later builds read reusable layers from it
and update it after a successful build.

The cache options are command options, so place them after `render` or
`render-one` and before `VERSION OS`. Also note that an existing final image is
skipped by default. Add `--force` when you intentionally want to rebuild it and
exercise the cache:

```bash
uv run render render-one --force 8.4 musl redis
```

### Select a Custom Cache Registry

The final image and cache may be stored in different registries. For example,
to publish the image to Docker Hub and its cache to GitHub Container Registry
(GHCR), pass `--cache-ref`.

For one extension, `--cache-ref` is the complete cache reference:

```bash
uv run render render-one \
  --force \
  --cache-ref ghcr.io/github_owner/docker-php-extension-cache:8.4-redis-musl \
  8.4 musl redis
```

For the batch `render` command, use a template so every extension gets its own
cache tag:

```bash
uv run render render \
  --force \
  --cache-ref 'ghcr.io/someblackmagic/docker-php-extension-images:cache-{version}-{ext}-{os}' \
  8.4 musl

./dst/builder-8.4-musl.sh
```

Keep the template in single quotes so the shell passes the braces unchanged.
The supported placeholders are:

- `{image}` — final image repository from `--image`;
- `{version}` — PHP version, for example `8.4`;
- `{ext}` — extension name, for example `redis`;
- `{os}` — OS variant, `glibc` or `musl`.

For the example above, the generated Redis build uses this cache reference:

```text
ghcr.io/github_owner/docker-php-extension-cache:8.4-redis-musl
```

Do not use one fixed cache reference for the entire batch. Separate tags avoid
extensions overwriting or polluting each other's caches.

### Disable the Cache

Pass `--no-cache` when no registry cache should be read or written:

```bash
uv run render render-one --no-cache 8.4 musl redis
uv run render render --no-cache 8.4 musl
```

`--no-cache` and `--cache-ref` cannot be used together.

### Authentication

Authenticate with every registry used by the build. For the default setup,
authenticate with Docker Hub:

```bash
docker login
```

When using GHCR for the cache, also create a GitHub token with `read:packages`
and `write:packages`, then authenticate with GHCR:

```bash
export GITHUB_USER="your-github-user"
export GITHUB_TOKEN="your-github-token"
echo "$GITHUB_TOKEN" | docker login ghcr.io \
  --username "$GITHUB_USER" \
  --password-stdin
```

Avoid putting the token directly in a command or committing it to the
repository. In CI, store it as a secret. GHCR repository names must be
lowercase; replace `github_owner` in the examples with your GitHub user or
organization.

### GitHub Actions Cache Backend

Buildx also supports `--cache-from type=gha` and `--cache-to type=gha,mode=max`
inside GitHub Actions. For the remote Buildx nodes configured in
`docs/SetupRunners.md`, the registry backend shown above is preferable because
the cache is stored as a normal GHCR package and is available to every
authenticated builder.

## Render an Aggregate Verification Dockerfile

The command syntax is:

```bash
uv run render aggregate [--image IMAGE] VERSION OS EXTENSION...
```

For example:

```bash
uv run render aggregate 7.4 musl \
  mysqli pdo_mysql propro raphf redis sockets zip http
```

The command only creates `var/Dockerfile`. The order of its `COPY --from`
instructions matches the extension order on the command line. Build the
verification image separately:

```bash
docker buildx build --progress plain --file var/Dockerfile .
```

For aggregate rendering, `musl` maps to the `php:<version>-alpine` base image.

## Alternative CLI Invocation

Run the CLI through the Makefile:

```bash
make render ARGS="render 8.4 musl"
```

After `uv sync`, the compatibility launcher can also be used:

```bash
uv run python render render 8.4 musl
```
