# -------------------- Installing PHP Extension: xsl --------------------
RUN set -eux \
    && install-php-extensions  xsl \
    && php -m | grep -oiE '^xsl$' \
    && true
