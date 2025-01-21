# -------------------- Installing PHP Extension: sockets --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add linux-headers \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) sockets \
    && php -m | grep -oiE '^sockets$' \
    && true
