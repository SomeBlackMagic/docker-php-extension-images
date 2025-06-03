# -------------------- Installing PHP Extension: psr --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && pecl install psr \
    # Enabling
    && install-php-extensions psr \
    && php -m | grep -oiE '^psr$' \
    && true
