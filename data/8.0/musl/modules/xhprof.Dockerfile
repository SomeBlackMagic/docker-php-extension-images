# -------------------- Installing PHP Extension: xhprof --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install xhprof \
    # Enabling
    && docker-php-ext-enable xhprof \
    && php -m | grep -oiE '^xhprof$' \
    && true
