# -------------------- Installing PHP Extension: vips --------------------
RUN set -eux \
    # Generic pre-command \
    && apk add vips-dev \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install vips \
    # Enabling
    && docker-php-ext-enable vips \
    && php -m | grep -oiE '^vips$' \
    && true
