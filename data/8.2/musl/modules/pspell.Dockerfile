# -------------------- Installing PHP Extension: pspell --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
#    && apk add aspell-dev \
    && install-php-extensions pspell \
    && php -m | grep -oiE '^pspell$' \
    && true
