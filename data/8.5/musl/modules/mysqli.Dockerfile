# -------------------- Installing PHP Extension: mysqli --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add libmcrypt-dev \
    && install-php-extensions mysqli \
    && php -m | grep -oiE '^mysqli$' \
    && true
