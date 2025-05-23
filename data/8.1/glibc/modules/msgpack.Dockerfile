# -------------------- Installing PHP Extension: msgpack --------------------
RUN set -eux \
    && install-php-extensions msgpack \
    && php -m | grep -oiE '^msgpack$' \
    && true
