# -------------------- Installing PHP Extension: xhprof --------------------
RUN set -eux \
    && install-php-extensions xhprof \
    && php -m | grep -oiE '^xhprof$' \
    && true
