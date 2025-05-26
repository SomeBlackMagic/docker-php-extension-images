# -------------------- Installing PHP Extension: sysvsem --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) sysvsem \
    && php -m | grep -oiE '^sysvsem$' \
    && true
