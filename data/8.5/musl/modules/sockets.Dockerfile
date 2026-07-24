# -------------------- Installing PHP Extension: sockets --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && apk add linux-headers \
    && install-php-extensions sockets \
    && php -m | grep -oiE '^sockets$' \
    && true
