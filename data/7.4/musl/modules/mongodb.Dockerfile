# -------------------- Installing PHP Extension: mongodb --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    # && apk add libressl-dev \
    # && pecl install mongodb-1.16.0 \
    # Enabling
    && install-php-extensions mongodb \
    && php -m | grep -oiE '^mongodb$' \
    && true
