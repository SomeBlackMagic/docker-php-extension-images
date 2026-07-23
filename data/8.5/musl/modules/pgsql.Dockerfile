# -------------------- Installing PHP Extension: pgsql --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && apk add postgresql-dev \
    && install-php-extensions pgsql \
    && php -m | grep -oiE '^pgsql$' \
    && true
