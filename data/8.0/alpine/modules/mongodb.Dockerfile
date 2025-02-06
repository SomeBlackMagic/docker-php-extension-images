# -------------------- Installing PHP Extension: mongodb --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && apk add libressl-dev \
    && pecl install mongodb \
    # Enabling
    && docker-php-ext-enable mongodb \
    && php -m | grep -oiE '^mongodb$' \
    && true
