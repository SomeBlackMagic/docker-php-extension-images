# -------------------- Installing PHP Extension: gmp --------------------
RUN set -eux \
    && install-php-extensions gmp \
    && php -m | grep -oiE '^gmp$' \
    && true
