# -------------------- Installing PHP Extension: xml --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && apk add libxml2-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) xml \
    && php -m | grep -oiE '^xml$' \
    && true
