# -------------------- Installing PHP Extension: shmop --------------------
RUN set -eux \
    && install-php-extensions shmop \
    && php -m | grep -oiE '^shmop$' \
    && true
