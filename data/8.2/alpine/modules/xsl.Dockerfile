# -------------------- Installing PHP Extension: xsl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libxslt-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) xsl \
    && php -m | grep -oiE '^xsl$' \
    && true
