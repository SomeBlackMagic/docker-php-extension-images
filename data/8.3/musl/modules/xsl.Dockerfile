# -------------------- Installing PHP Extension: xsl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add libxslt-dev \
    && install-php-extensions xsl \
    && php -m | grep -oiE '^xsl$' \
    && true
