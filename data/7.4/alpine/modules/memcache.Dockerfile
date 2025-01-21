# -------------------- Installing PHP Extension: memcache --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libzip-dev \
    && pecl install memcache-4.0.5.2 \
    && docker-php-ext-enable memcache \
    && php -m | grep -oiE '^memcache$' \
    && true
