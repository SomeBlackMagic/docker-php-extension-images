# -------------------- Installing PHP Extension: sysvsem --------------------
RUN set -eux \
    && install-php-extensions sysvsem \
    && php -m | grep -oiE '^sysvsem$' \
    && true
