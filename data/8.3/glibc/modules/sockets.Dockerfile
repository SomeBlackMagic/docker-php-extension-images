# -------------------- Installing PHP Extension: sockets --------------------
RUN set -eux \
    && install-php-extensions sockets \
    && php -m | grep -oiE '^sockets$' \
    && true
