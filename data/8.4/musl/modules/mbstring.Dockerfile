# -------------------- Installing PHP Extension: mbstring --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension \
    && apk add libmcrypt-dev oniguruma-dev\
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) mbstring \
    && php -m | grep -oiE '^mbstring$' \
    && true
