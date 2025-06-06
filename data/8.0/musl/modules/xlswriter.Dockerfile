# -------------------- Installing PHP Extension: xlswriter --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
#    && apk add libzip-dev \
#    && pecl install xlswriter \
    # Enabling
    && install-php-extensions xlswriter \
    && php -m | grep -oiE '^xlswriter$' \
    && true
