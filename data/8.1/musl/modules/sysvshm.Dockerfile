# -------------------- Installing PHP Extension: sysvshm --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && install-php-extensions sysvshm \
    && php -m | grep -oiE '^sysvshm$' \
    && true
