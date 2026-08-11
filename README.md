# Docker PHP Extension Images

[![Docker Hub](https://img.shields.io/docker/pulls/someblackmagic/docker-php-extension-images)](https://hub.docker.com/r/someblackmagic/docker-php-extension-images)

Docker PHP Extension Images provide pre-compiled PHP extensions for various PHP versions and architectures. These images simplify the integration of PHP extensions into your projects by eliminating the need for local compilation.

## Table of Contents

- [Features](#features)
- [Supported PHP Versions](#supported-php-versions)
- [Supported Systems](#supported-systems)
- [Supported Architectures](#supported-architectures)
- [Usage](#usage)
    - [Pulling the Image](#pulling-the-image)
    - [Copying Extensions](#copying-extensions)
- [Examples](#example)
- [License](#license)

## Features

- **Pre-compiled Extensions:** Save time by using pre-compiled PHP extensions.
- **Multiple PHP Versions:** Supports PHP versions from 7.4 up to 8.5.
- **Alpine and Debian Base:** Currently available for Alpine Linux with plans to support Debian.
- **Multi-Architecture Support:** Compiled for both `amd64` and `arm64`, ensuring compatibility with MacOS and various server environments.
- **Easy Integration:** Simple Docker commands to integrate extensions into your projects without local compilation.

## Supported PHP Versions

- PHP 7.4
- PHP 8.0
- PHP 8.1
- PHP 8.2
- PHP 8.3
- PHP 8.4
- PHP 8.5

## Supported Systems

- **Alpine Linux:** Lightweight and secure base image.
- **Debian (Planned):** Upcoming support for Debian-based images.

## Supported Architectures

- `amd64`
- `arm64`

## Usage

### Pulling the Image

Pull the desired PHP extension image from Docker Hub:

```bash
docker pull someblackmagic/docker-php-extension-images:<php-version>-<extension>-<system>
```
#### Example:
```bash 
docker pull someblackmagic/docker-php-extension-images:8.2-mcrypt-alpine
```


### Copying Extensions
Use the COPY --from directive in your Dockerfile to include the compiled extensions in your project image.
```bash
COPY --from=someblackmagic/docker-php-extension-images:<php-version>-<extension>-<system> /path/to/extensions /path/in/your/image
```
or

```bash
COPY --from=someblackmagic/docker-php-extension-images:<php-version>-<extension>-<system> / /
```

#### Example:
```Docker


FROM php:8.2-fpm-alpine

RUN set -eux \
    && apk upgrade --available \
    && apk add curl autoconf build-base autoconf automake git gcc make g++  \
    && true

# Copy mcrypt extension from the pre-built image
COPY --from=someblackmagic/docker-php-extension-images:8.2-mcrypt-alpine / /


```

### Using Multiple Extensions
If you need multiple extensions, you can copy them from different pre-built images or create a custom image that includes all required extensions.
```Docker

FROM php:8.2-fpm-alpine

RUN set -eux \
    && apk upgrade --available \
    && apk add curl autoconf build-base autoconf automake git gcc make g++  \
    && true

# Copy mcrypt extension
COPY --from=someblackmagic/docker-php-extension-images:8.2-mcrypt-alpine / /

# Copy another extension, e.g., xdebug
COPY --from=someblackmagic/docker-php-extension-images:8.2-xdebug-alpine / /

```

### Generating an Aggregate Verification Dockerfile

Generate `var/Dockerfile` from an explicit, ordered extension list:

```bash
uv run render aggregate 7.4 musl mysqli pdo_mysql propro raphf redis sockets zip http
```

Use `--image` to select a different image repository. The extension order in the
generated Dockerfile matches the command-line order.

### Registry Build Cache

The `render` and `render-one` commands use an isolated BuildKit registry cache
for every extension by default. Disable it with `--no-cache`, or provide a custom
reference with `--cache-ref`:

```bash
uv run render render-one --cache-ref registry.example.com/php:redis-cache 8.4 musl redis
uv run render render --cache-ref '{image}:buildcache-{version}-{ext}-{os}' 8.4 musl
```

Batch cache templates support `{image}`, `{version}`, `{ext}`, and `{os}`.
Registry authentication is read from the existing Docker configuration.

### Logging

Add `-v` before the command to see high-level progress logs, or `-vv` for
detailed diagnostics such as generated Docker commands and image status:

```bash
uv run render -v render 8.4 musl
uv run render -vv render-one 8.4 musl redis
```

Logs are written to standard error and normal command output remains unchanged.

### Development Tests

Run the complete deterministic test suite with coverage:

```bash
uv run pytest tests/ -v --cov=docker_render --cov-report=term-missing
```


### License
This project is licensed under the MIT License.
