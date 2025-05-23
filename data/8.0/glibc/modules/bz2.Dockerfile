# -------------------- Installing PHP Extension: bz2 --------------------
RUN set -eux \
    && install-php-extensions bz2 \
    && php -m | grep -oiE '^bz2$' \
    && true
