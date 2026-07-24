# -------------------- Installing PHP Extension: ast --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Custom:       Pecl command
#    && pecl install ast \
    # Enabling
    && install-php-extensions ast \
    && php -m | grep -oiE '^ast$' \
    && true
