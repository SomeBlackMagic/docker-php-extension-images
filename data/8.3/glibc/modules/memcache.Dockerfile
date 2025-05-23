# -------------------- Installing PHP Extension: memcache --------------------
RUN set -eux \
    && install-php-extensions memcache \
    && php -m | grep -oiE '^memcache$' \
    && true
