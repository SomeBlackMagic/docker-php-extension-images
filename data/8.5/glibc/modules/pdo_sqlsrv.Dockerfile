# -------------------- Installing PHP Extension: pdo_sqlsrv --------------------
RUN set -eux \
    && install-php-extensions pdo_sqlsrv \
    && php -m | grep -oiE '^pdo_sqlsrv$' \
    && true
