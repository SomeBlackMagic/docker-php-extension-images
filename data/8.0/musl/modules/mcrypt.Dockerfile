# -------------------- Installing PHP Extension: mcrypt --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add libmcrypt-dev \
    && pecl install mcrypt \
    && docker-php-ext-enable mcrypt \
    && php -m | grep -oiE '^mcrypt$' \
    && true
