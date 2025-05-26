# -------------------- Installing PHP Extension: ssh2 --------------------
RUN set -eux \
    # Installation: Generic \
    && apk add libssh2-dev \
    # Type:         PECL extension
    # Default:      Pecl command
    && pecl install ssh2-1.3.1 \
    # Enabling
    && docker-php-ext-enable ssh2 \
    && php -m | grep -oiE '^ssh2$' \
    && true
