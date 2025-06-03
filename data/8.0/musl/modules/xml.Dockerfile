# -------------------- Installing PHP Extension: xml --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && apk add libxml2-dev \
    && install-php-extensions xml \
    && php -m | grep -oiE '^xml$' \
    && true
