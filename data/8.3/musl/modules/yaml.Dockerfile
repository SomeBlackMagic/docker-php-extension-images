# -------------------- Installing PHP Extension: yaml --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
#    && apk add yaml-dev \
#    && pecl install yaml \
    # Enabling
    && install-php-extensions yaml \
    && php -m | grep -oiE '^yaml$' \
    && true
