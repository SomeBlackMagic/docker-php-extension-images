# -------------------- Installing PHP Extension: gettext --------------------
RUN set -eux \
    && install-php-extensions gettext \
    && php -m | grep -oiE '^gettext' \
    && true
