# -------------------- Installing PHP Extension: swoole --------------------
RUN set -eux \
    && install-php-extensions swoole \
    && php -m | grep -oiE '^swoole$' \
    && true
