# -------------------- Installing PHP Extension: redis --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install redis \
    # Enabling
    && docker-php-ext-enable redis \
    && php -m | grep -oiE '^redis$' \
    && true
