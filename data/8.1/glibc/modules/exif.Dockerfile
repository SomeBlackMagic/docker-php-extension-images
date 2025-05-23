# -------------------- Installing PHP Extension: exif --------------------
RUN set -eux \
    && install-php-extensions exif \
    && php -m | grep -oiE '^exif$' \
    && true
