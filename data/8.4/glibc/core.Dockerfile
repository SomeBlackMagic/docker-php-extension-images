FROM php:8.4-bookworm AS builder

COPY --from=ghcr.io/mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/local/bin/
COPY --from=bitnami/git:2-debian-12 / /tmp/bitnami-git


RUN set -eux \
    && ln -s /tmp/bitnami-git/opt/bitnami/git/bin/git /usr/local/bin/git \
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
