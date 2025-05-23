# -------------------- Installing PHP Extension: vips --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
    && apk add pkgconf vips-dev \
    && pecl install vips \
    # Enabling
    && docker-php-ext-enable vips \
    && true
