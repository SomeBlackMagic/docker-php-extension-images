# -------------------- Installing PHP Extension: gettext --------------------
RUN set -eux \
    && install-php-extensions excimer \
    && php -m | grep -oiE '^excimer' \
    && true
