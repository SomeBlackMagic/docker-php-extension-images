# -------------------- Installing PHP Extension: redis --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && pecl install redis \
    # Enabling
    && install-php-extensions redis \
    && php -m | grep -oiE '^redis$' \
    && true
