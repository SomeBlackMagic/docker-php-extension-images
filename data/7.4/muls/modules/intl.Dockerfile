# -------------------- Installing PHP Extension: intl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add icu-dev libstdc++ \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) intl \
    && php -m | grep -oiE '^intl$' \
    && true
