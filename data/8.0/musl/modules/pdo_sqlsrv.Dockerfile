# -------------------- Installing PHP Extension: pdo_sqlsrv --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add unixodbc-dev \
    && pecl install pdo_sqlsrv-5.9.0 \
    # Enabling
    && docker-php-ext-enable pdo_sqlsrv \
    && php -m | grep -oiE '^pdo_sqlsrv$' \
    && true
