# -------------------- Installing PHP Extension: propro$ --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
    && pecl install propro \
    && docker-php-ext-enable propro \
    && php -m | grep -oiE '^propro$' \
    && true




