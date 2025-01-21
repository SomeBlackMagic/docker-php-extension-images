# -------------------- Installing PHP Extension: pdo_mysql --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    # Custom:       configure command
    && docker-php-ext-configure pdo_mysql --with-zlib-dir=/usr \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pdo_mysql \
    && php -m | grep -oiE '^pdo_mysql$' \
    && true
