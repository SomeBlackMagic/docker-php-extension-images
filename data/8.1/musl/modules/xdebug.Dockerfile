# -------------------- Installing PHP Extension: xdebug --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && apk add --update linux-headers \
#    && pecl install xdebug-3.1.6 \
    # Enabling
    && install-php-extensions xdebug \
    && php -m | grep -oiE '^xdebug$' \
    && true
