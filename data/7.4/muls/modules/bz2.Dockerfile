# -------------------- Installing PHP Extension: bz2 --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add bzip2-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) bz2 \
    && php -m | grep -oiE '^bz2$' \
    && true
