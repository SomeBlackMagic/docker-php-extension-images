# -------------------- Installing PHP Extension: xdebug --------------------
RUN set -eux \
    && install-php-extensions xdebug \
    && php -m | grep -oiE '^xdebug$' \
    && true
