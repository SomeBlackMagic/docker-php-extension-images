# -------------------- Installing PHP Extension: pdo_dblib --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add freetds-dev freetds \
    && install-php-extensions pdo_dblib \
    && php -m | grep -oiE '^pdo_dblib$' \
    && true
