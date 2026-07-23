# -------------------- Installing PHP Extension: msgpack --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && pecl install msgpack \
    # Enabling
    && install-php-extensions msgpack \
    && php -m | grep -oiE '^msgpack$' \
    && true
