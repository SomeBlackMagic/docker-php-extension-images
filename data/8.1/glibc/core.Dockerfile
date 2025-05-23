FROM php:8.1 AS builder

RUN set -eux \
    && apt update \
    && apt install -y curl autoconf autoconf automake git gcc make g++ \
    && true

ADD --chmod=0755 \
  https://github.com/mlocati/docker-php-extension-installer/releases/download/2.6.3/install-php-extensions \
  /usr/local/bin/

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
    # Installation: Generic
    # Type:         Built-in extension
    && (git ls-files --others --exclude-standard; git diff --name-only --cached --diff-filter=A) | sort -u | while IFS= read -r file; do cp -v --parents "/${file}" /opt; done \
    && true

FROM scratch
COPY --from=builder /opt /
