# -------------------- Installing PHP Extension: bcmath --------------------
RUN set -eux \
    && install-php-extensions bcmath \
    && php -m | grep -oiE '^bcmath' \
    && true
