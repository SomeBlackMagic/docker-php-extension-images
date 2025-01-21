# -------------------- Installing PHP Extension: exif --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) exif \
    && php -m | grep -oiE '^exif$' \
    && true
