# -------------------- Installing PHP Extension: mbstring --------------------
RUN set -eux \
    && install-php-extensions mbstring \
    && php -m | grep -oiE '^mbstring$' \
    && true
