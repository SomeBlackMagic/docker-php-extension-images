# -------------------- Installing PHP Extension: imagick --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add imagemagick imagemagick-dev ghostscript ghostscript-dev libpng libjpeg-turbo freetype-dev libpng-dev libjpeg-turbo-dev \
    # Enabling
    && pecl install imagick \
    && docker-php-ext-enable imagick \
    && php -m | grep -oiE '^imagick$' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'PNG' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'JPEG' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'PDF' \
    && true
