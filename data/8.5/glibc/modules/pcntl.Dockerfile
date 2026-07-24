# -------------------- Installing PHP Extension: pcntl --------------------
RUN set -eux \
    && install-php-extensions pcntl \
    && php -m | grep -oiE '^pcntl$' \
    && true
