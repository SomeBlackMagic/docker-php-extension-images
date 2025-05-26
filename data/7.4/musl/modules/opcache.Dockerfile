# -------------------- Installing PHP Extension: opcache --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) opcache \
#    && php -m | grep -oiE '^OPcache$' \
    && true
