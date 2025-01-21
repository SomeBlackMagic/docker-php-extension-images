# -------------------- Installing PHP Extension: pgsql --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add postgresql-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pgsql \
    && php -m | grep -oiE '^pgsql$' \
    && true
