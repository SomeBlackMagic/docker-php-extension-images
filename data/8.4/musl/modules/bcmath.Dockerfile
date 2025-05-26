# -------------------- Installing PHP Extension: bcmath --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) bcmath \
    && php -m | grep -oiE '^bcmath$' \
    && true
