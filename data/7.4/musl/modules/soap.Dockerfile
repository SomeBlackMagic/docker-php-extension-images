# -------------------- Installing PHP Extension: soap --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libxml2-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) soap \
    && php -m | grep -oiE '^soap$' \
    && true
