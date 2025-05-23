# -------------------- Installing PHP Extension: ast --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Custom:       Pecl command
    && pecl install ast \
    # Enabling
    && docker-php-ext-enable ast \
    && php -m | grep -oiE '^ast$' \
    && true
