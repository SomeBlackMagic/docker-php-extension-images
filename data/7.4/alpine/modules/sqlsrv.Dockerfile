# -------------------- Installing PHP Extension: sqlsrv --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && apk add unixodbc-dev \
    && pecl install sqlsrv-5.10.0 \
    # Enabling
    && docker-php-ext-enable sqlsrv \
    && php -m | grep -oiE '^sqlsrv$' \
    && true
