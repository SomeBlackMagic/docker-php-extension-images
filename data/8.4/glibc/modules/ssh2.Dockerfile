# -------------------- Installing PHP Extension: ssh2 --------------------
RUN set -eux \
    && install-php-extensions ssh2 \
    && php -m | grep -oiE '^ssh2$' \
    && true
