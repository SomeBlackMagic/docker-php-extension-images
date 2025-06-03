# -------------------- Installing PHP Extension: soap --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add libxml2-dev \
    && install-php-extensions soap \
    && php -m | grep -oiE '^soap$' \
    && true
