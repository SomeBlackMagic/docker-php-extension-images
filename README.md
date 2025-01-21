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
- **Multiple PHP Versions:** Supports PHP versions from 7.4 up to 8.3.
- **Alpine and Debian Base:** Currently available for Alpine Linux with plans to support Debian.
- **Multi-Architecture Support:** Compiled for both `amd64` and `arm64`, ensuring compatibility with MacOS and various server environments.
- **Easy Integration:** Simple Docker commands to integrate extensions into your projects without local compilation.

## Supported PHP Versions

- PHP 7.4
- PHP 8.0
- PHP 8.1
- PHP 8.2
- PHP 8.3

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


### License
This project is licensed under the MIT License.
