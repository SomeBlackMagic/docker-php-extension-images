FROM alpine:3.20 as git-static

# Установим зависимости
RUN apk add --no-cache \
    build-base \
    curl \
    curl-dev \
    musl-dev \
    openssl-dev \
    openssl-libs-static \
    zlib-dev \
    zlib-static \
    expat-dev \
    gettext \
    perl \
    tar \
    autoconf
# Установим переменные
ENV GIT_VERSION=2.44.0

# Скачиваем и компилируем Git статически
RUN curl -LO https://mirrors.edge.kernel.org/pub/software/scm/git/git-${GIT_VERSION}.tar.gz && \
    tar -xzf git-${GIT_VERSION}.tar.gz && \
    cd git-${GIT_VERSION} && \
    make configure && \
    ./configure \
        --prefix=/usr/local/git-static \
        --with-openssl \
        --with-curl \
        --with-zlib \
        CFLAGS="-static -O2" \
        LDFLAGS="-static" && \
    make -j$(nproc) && \
    make install


FROM php:7.4-alpine AS builder

COPY --from=ghcr.io/mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/local/bin/
COPY --from=git-static /usr/local/git-static /usr/local/git-static

RUN set -eux \
    && apk upgrade --available \
    && apk add autoconf gcc build-base \
    && true

RUN set -eux \
    && ln -s /usr/local/git-static/bin/git /usr/local/bin/git \
    && true

USER root
WORKDIR /

COPY <<EOF .gitignore
/proc
/sys
/dev
/run
/tmp
/etc
/root
/var
EOF

RUN set -eux \
    && git config --global init.defaultBranch master \
    && git config --global --add safe.directory / \
    && git config --global user.email "root@localhost"  \
    && git config --global user.name "root" \
    && git init \
    && git add . \
    && git commit -m "core" \
    && true


{{ module | raw }}


RUN set -eux \
    && (git ls-files --others --exclude-standard; git diff --name-only --cached --diff-filter=A) | sort -u | while IFS= read -r file; do cp -v --parents "/${file}" /opt; done \
    && true

FROM scratch
COPY --from=builder /opt /
