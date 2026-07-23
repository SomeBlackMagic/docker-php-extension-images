# -------------------- Installing PHP Extension: pspell --------------------
RUN set -eux \
    && install-php-extensions pspell \
    && php -m | grep -oiE '^pspell$' \
    && true
