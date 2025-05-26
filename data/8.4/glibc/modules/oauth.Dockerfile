# -------------------- Installing PHP Extension: oauth --------------------
RUN set -eux \
    && install-php-extensions oauth \
    && php -m | grep -oiE '^oauth$' \
    && true
