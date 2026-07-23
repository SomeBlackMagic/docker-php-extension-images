# -------------------- Installing PHP Extension: sysvmsg --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && install-php-extensions sysvmsg \
    && php -m | grep -oiE '^sysvmsg$' \
    && true
