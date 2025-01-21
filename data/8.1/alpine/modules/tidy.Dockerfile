# -------------------- Installing PHP Extension: tidy --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add tidyhtml-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) tidy \
    && php -m | grep -oiE '^tidy$' \
    && true
