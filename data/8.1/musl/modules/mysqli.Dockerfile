# -------------------- Installing PHP Extension: mysqli --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libmcrypt-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) mysqli \
    && php -m | grep -oiE '^mysqli$' \
    && true
