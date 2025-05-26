# -------------------- Installing PHP Extension: pdo_dblib --------------------
RUN set -eux \
    && install-php-extensions pdo_dblib \
    && php -m | grep -oiE '^pdo_dblib$' \
    && true
