# -------------------- Installing PHP Extension: gmp --------------------
RUN set -eux \
#    # Installation: Generic
#    && apk add gmp-dev \
#    # Type:         Built-in extension
#    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) gmp \
    && install-php-extensions gmp \
    && php -m | grep -oiE '^gmp$' \
    && true
