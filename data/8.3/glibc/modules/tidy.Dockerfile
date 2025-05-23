# -------------------- Installing PHP Extension: tidy --------------------
RUN set -eux \
    && install-php-extensions tidy \
    && php -m | grep -oiE '^tidy$' \
    && true
