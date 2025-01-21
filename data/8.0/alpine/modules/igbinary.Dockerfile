# -------------------- Installing PHP Extension: igbinary --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install igbinary \
    # Enabling
    && docker-php-ext-enable igbinary \
    && php -m | grep -oiE '^igbinary$' \
    && true
