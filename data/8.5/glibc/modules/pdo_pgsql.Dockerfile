# -------------------- Installing PHP Extension: pdo_pgsql --------------------
RUN set -eux \
    && install-php-extensions pdo_pgsql \
    && php -m | grep -oiE '^pdo_pgsql$' \
    && true
