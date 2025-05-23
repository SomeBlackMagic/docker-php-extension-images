# -------------------- Installing PHP Extension: pcntl --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) pcntl \
    && php -m | grep -oiE '^pcntl$' \
    && true
