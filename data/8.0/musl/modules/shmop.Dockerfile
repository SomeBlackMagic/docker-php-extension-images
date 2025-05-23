# -------------------- Installing PHP Extension: shmop --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) shmop \
    && php -m | grep -oiE '^shmop$' \
    && true
