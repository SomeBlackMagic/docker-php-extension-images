# -------------------- Installing PHP Extension: soap --------------------
RUN set -eux \
    && install-php-extensions soap \
    && php -m | grep -oiE '^soap$' \
    && true
