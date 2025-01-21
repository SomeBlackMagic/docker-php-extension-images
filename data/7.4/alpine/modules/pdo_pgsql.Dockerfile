# -------------------- Installing PHP Extension: pdo_pgsql --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add postgresql-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pdo_pgsql \
    && php -m | grep -oiE '^pdo_pgsql$' \
    && true
