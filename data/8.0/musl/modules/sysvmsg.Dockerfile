# -------------------- Installing PHP Extension: sysvmsg --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) sysvmsg \
    && php -m | grep -oiE '^sysvmsg$' \
    && true
