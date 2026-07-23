# -------------------- Installing PHP Extension: mcrypt --------------------
RUN set -eux \
    && install-php-extensions mcrypt \
    && php -m | grep -oiE '^mcrypt$' \
    && true
