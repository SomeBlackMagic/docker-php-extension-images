# -------------------- Installing PHP Extension: vips --------------------
RUN set -eux \
    && install-php-extensions vips \
    && php -m | grep -oiE '^vips$' \
    && true
