# -------------------- Installing PHP Extension: curl --------------------
RUN set -eux \
    && install-php-extensions curl \
    && php -m | grep -oiE '^curl$' \
    && true
