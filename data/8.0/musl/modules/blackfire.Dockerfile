# -------------------- Installing PHP Extension: blackfire --------------------
RUN set -eux \
    && install-php-extensions blackfire \
    && php -m | grep -oiE '^blackfire$' \
    && true
