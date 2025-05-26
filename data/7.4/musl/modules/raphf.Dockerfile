# -------------------- Installing PHP Extension: raphf --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && pecl install raphf \
    # Enabling
    && docker-php-ext-enable raphf \
    && php -m | grep -oiE '^raphf$' \
    && true
