# -------------------- Installing PHP Extension: sysvshm --------------------
RUN set -eux \
    && install-php-extensions sysvshm \
    && php -m | grep -oiE '^sysvshm$' \
    && true
