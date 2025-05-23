# -------------------- Installing PHP Extension: igbinary --------------------
RUN set -eux \
    && install-php-extensions igbinary \
    && php -m | grep -oiE '^igbinary$' \
    && true
