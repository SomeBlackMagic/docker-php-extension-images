# -------------------- Installing PHP Extension: pdo_pgsql --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add postgresql-dev \
    && install-php-extensions pdo_pgsql \
    && php -m | grep -oiE '^pdo_pgsql$' \
    && true
