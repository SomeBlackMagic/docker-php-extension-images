# -------------------- Installing PHP Extension: memcached --------------------
RUN set -eux \
    && install-php-extensions memcached \
    && php -m | grep -oiE '^memcached$' \
    && true
