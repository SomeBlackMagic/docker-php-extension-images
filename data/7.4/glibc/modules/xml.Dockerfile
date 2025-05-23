# -------------------- Installing PHP Extension: xml --------------------
RUN set -eux \
    && install-php-extensions xml \
    && php -m | grep -oiE '^xml$' \
    && true
