# -------------------- Installing PHP Extension: gettext --------------------
RUN set -eux \
    && install-php-extensions excimer \
    && php -m | grep -oiE '^excimer' \
    && true

uv run render render-one --force --cache-ref 'ghcr.io/someblackmagic/docker-php-extension-images:cache-{version}-{ext}-{os}' 8.5 musl excimer
