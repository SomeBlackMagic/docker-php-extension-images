# -------------------- Installing PHP Extension: sysvsem --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && install-php-extensions sysvsem \
    && php -m | grep -oiE '^sysvsem$' \
    && true
