# -------------------- Installing PHP Extension: psr --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install psr \
    # Enabling
    && docker-php-ext-enable psr \
    && php -m | grep -oiE '^psr$' \
    && true
