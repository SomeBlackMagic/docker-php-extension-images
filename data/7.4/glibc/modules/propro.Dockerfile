# -------------------- Installing PHP Extension: propro$ --------------------
RUN set -eux \
    && install-php-extensions propro \
    && php -m | grep -oiE '^propro$' \
    && true




