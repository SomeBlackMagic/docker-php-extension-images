# -------------------- Installing PHP Extension: gd --------------------
RUN set -eux \
    && install-php-extensions gd \
    && php -m | grep -oiE '^gd$' \
    && true
