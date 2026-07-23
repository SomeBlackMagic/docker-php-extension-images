# -------------------- Installing PHP Extension: redis --------------------
RUN set -eux \
    && install-php-extensions redis \
    && php -m | grep -oiE '^redis$' \
    && true
