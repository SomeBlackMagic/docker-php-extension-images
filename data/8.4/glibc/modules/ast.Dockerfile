# -------------------- Installing PHP Extension: ast --------------------
RUN set -eux \
    && install-php-extensions ast \
    && php -m | grep -oiE '^ast$' \
    && true
