# -------------------- Installing PHP Extension: oauth --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
#    && apk add pcre-dev \
#    && pecl install oauth \
    # Enabling
    && install-php-extensions oauth \
    && php -m | grep -oiE '^oauth$' \
    && true
