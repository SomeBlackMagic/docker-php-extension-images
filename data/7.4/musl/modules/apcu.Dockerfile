# -------------------- Installing PHP Extension: apcu --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && pecl install apcu \
    # Enabling
    && install-php-extensions apcu \
    && php -m | grep -oiE '^apcu' \
    && true
