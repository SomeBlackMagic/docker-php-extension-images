# -------------------- Installing PHP Extension: propro$ --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && pecl install propro \
    && install-php-extensions propro \
    && php -m | grep -oiE '^propro$' \
    && true




