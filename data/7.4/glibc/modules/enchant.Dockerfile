# -------------------- Installing PHP Extension: enchant --------------------
RUN set -eux \
    && install-php-extensions enchant \
    && php -m | grep -oiE '^enchant$' \
    && true

