# -------------------- Installing PHP Extension: imagick --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add pkgconfig  imagemagick-dev \
    # Enabling
    && pecl install imagick \
    && docker-php-ext-enable imagick \
    && php -m | grep -oiE '^imagick$' \
    && true
