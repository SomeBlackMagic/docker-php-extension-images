# -------------------- Installing PHP Extension: sysvshm --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) sysvshm \
    && php -m | grep -oiE '^sysvshm$' \
    && true
