# -------------------- Installing PHP Extension: calendar --------------------
RUN set -eux \
    && install-php-extensions  calendar \
    && php -m | grep -oiE '^calendar$' \
    && true
