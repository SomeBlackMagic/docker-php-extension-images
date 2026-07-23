# -------------------- Installing PHP Extension: apcu --------------------
RUN set -eux \
    && install-php-extensions apcu \
    && php -m | grep -oiE '^apcu' \
    && true
