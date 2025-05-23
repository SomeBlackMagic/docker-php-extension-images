# -------------------- Installing PHP Extension: sqlsrv --------------------
RUN set -eux \
    && install-php-extensions sqlsrv \
    && php -m | grep -oiE '^sqlsrv$' \
    && true
