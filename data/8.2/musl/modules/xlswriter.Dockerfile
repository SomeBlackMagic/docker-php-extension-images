# -------------------- Installing PHP Extension: xlswriter --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add libzip-dev \
    && pecl install xlswriter \
    # Enabling
    && docker-php-ext-enable xlswriter \
    && php -m | grep -oiE '^xlswriter$' \
    && true
