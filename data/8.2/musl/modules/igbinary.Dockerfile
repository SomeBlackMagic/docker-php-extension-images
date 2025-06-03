# -------------------- Installing PHP Extension: igbinary --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && pecl install igbinary \
    # Enabling
    && install-php-extensions igbinary \
    && php -m | grep -oiE '^igbinary$' \
    && true

