# -------------------- Installing PHP Extension: dba --------------------
RUN set -eux \
    && install-php-extensions dba \
    && php -m | grep -oiE '^dba$' \
    && true
