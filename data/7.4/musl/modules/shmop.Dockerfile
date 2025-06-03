# -------------------- Installing PHP Extension: shmop --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && install-php-extensions shmop \
    && php -m | grep -oiE '^shmop$' \
    && true
