FROM php:8.3-alpine AS git-core

RUN set -eux \
    && apk update \
    && apk add git \
    && true


COPY --from=php:8.3-bullseye / /opt

COPY --from=ghcr.io/mlocati/php-extension-installer /usr/bin/install-php-extensions /opt/usr/local/bin/

USER root
WORKDIR /opt

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


FROM php:8.3-alpine as builder-temp

COPY --from=ghcr.io/mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/local/bin/

COPY --from=git-core /opt/.git /.git
COPY --from=git-core /opt/.gitignore /.gitignore

{{ module | raw }}

FROM git-core as artifacts

RUN rm -f /opt/var/lock

COPY --from=builder-temp / /opt/

WORKDIR /opt

RUN set -eux \
    && mkdir /dst \
    && (git ls-files --others --exclude-standard; git diff --name-only --cached --diff-filter=A) | sort -u | while IFS= read -r file; do cp -v --parents "/opt/${file}" /dst; done \
    && true

FROM scratch
COPY --from=artifacts /dst/opt /
