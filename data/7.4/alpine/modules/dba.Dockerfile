# -------------------- Installing PHP Extension: dba --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) dba \
    && php -m | grep -oiE '^dba$' \
    && true
