# -------------------- Installing PHP Extension: calendar --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) calendar \
    && php -m | grep -oiE '^calendar$' \
    && true
