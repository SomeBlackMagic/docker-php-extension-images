# -------------------- Installing PHP Extension: xdebug --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && apk add --update linux-headers \
    && pecl install xdebug \
    # Enabling
    && docker-php-ext-enable xdebug \
    && php -m | grep -oiE '^xdebug$' \
    && true
