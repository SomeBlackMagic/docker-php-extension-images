# -------------------- Installing PHP Extension: intl --------------------
RUN set -eux \
    && install-php-extensions intl \
    && php -m | grep -oiE '^intl$' \
    && true
