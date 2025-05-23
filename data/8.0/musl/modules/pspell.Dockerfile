# -------------------- Installing PHP Extension: pspell --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add aspell-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pspell \
    && php -m | grep -oiE '^pspell$' \
    && true
