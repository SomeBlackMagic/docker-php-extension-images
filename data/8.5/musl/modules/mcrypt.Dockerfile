# -------------------- Installing PHP Extension: mcrypt --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && apk add libmcrypt-dev \
#    && pecl install mcrypt \
    && install-php-extensions mcrypt \
    && php -m | grep -oiE '^mcrypt$' \
    && true
