# -------------------- Installing PHP Extension: mysqli --------------------
RUN set -eux \
    && install-php-extensions mysqli \
    && php -m | grep -oiE '^mysqli$' \
    && true
