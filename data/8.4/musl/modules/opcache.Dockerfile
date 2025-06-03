# -------------------- Installing PHP Extension: opcache --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && install-php-extensions opcache \
#    && php -m | grep -oiE '^OPcache$' \
    && true
