# -------------------- Installing PHP Extension: oauth --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add pcre-dev \
    && pecl install oauth \
    # Enabling
    && docker-php-ext-enable oauth \
    && php -m | grep -oiE '^oauth$' \
    && true
