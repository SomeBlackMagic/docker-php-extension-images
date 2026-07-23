# -------------------- Installing PHP Extension: pgsql --------------------
RUN set -eux \
    && install-php-extensions pgsql \
    && php -m | grep -oiE '^pgsql$' \
    && true
