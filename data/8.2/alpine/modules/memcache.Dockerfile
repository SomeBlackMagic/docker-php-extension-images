# -------------------- Installing PHP Extension: memcache --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libzip-dev \
    && pecl install memcache-8.0 \
    && docker-php-ext-enable memcache \
    && php -m | grep -oiE '^memcache$' \
    && true
