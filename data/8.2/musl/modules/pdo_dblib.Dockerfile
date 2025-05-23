# -------------------- Installing PHP Extension: pdo_dblib --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add freetds-dev freetds \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pdo_dblib \
    && php -m | grep -oiE '^pdo_dblib$' \
    && true
