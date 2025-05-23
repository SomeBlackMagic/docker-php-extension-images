# -------------------- Installing PHP Extension: sysvmsg --------------------
RUN set -eux \
    && install-php-extensions sysvmsg \
    && php -m | grep -oiE '^sysvmsg$' \
    && true
