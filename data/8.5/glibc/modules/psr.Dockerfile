# -------------------- Installing PHP Extension: psr --------------------
RUN set -eux \
    && install-php-extensions psr \
    && php -m | grep -oiE '^psr$' \
    && true
