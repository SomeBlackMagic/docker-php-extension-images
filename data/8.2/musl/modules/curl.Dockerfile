# -------------------- Installing PHP Extension: intl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add curl-dev curl \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) curl \
    && php -m | grep -oiE '^curl$' \
    && true
