# -------------------- Installing PHP Extension: uploadprogress --------------------
RUN set -eux \
    && install-php-extensions uploadprogress \
    && php -m | grep -oiE '^uploadprogress$' \
    && true
