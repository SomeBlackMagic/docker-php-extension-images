# -------------------- Installing PHP Extension: zip --------------------
RUN set -eux \
    && install-php-extensions zip \
    && php -m | grep -oiE '^zip$' \
    && true
