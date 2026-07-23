# -------------------- Installing PHP Extension: pecl --------------------
RUN set -eux \
    && install-php-extensions maxminddb \
    && php -m | grep -oiE '^maxminddb$' \
    && true
