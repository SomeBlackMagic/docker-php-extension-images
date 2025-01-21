# -------------------- Installing PHP Extension: gettext --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add gettext-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) gettext \
    && php -m | grep -oiE '^gettext' \
    && true
