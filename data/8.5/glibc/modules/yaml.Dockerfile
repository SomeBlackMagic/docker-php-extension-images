# -------------------- Installing PHP Extension: yaml --------------------
RUN set -eux \
    && install-php-extensions  yaml \
    && php -m | grep -oiE '^yaml$' \
    && true
