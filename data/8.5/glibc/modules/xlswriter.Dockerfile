# -------------------- Installing PHP Extension: xlswriter --------------------
RUN set -eux \
    && install-php-extensions xlswriter \
    && php -m | grep -oiE '^xlswriter$' \
    && true
