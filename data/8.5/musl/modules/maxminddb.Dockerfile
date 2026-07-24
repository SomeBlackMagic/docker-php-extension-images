# -------------------- Installing PHP Extension: pecl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
#    && apk add libmaxminddb-dev \
#    && pecl install maxminddb \
    # Enabling
    && install-php-extensions maxminddb \
    && php -m | grep -oiE '^maxminddb$' \
    && true
