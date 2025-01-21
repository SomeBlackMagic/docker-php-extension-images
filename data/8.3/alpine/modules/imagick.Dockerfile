# -------------------- Installing PHP Extension: imagick --------------------
# https://github.com/Imagick/imagick/issues/640
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add pkgconfig  imagemagick-dev \
    # Enabling
    && install-php-extensions imagick/imagick@28f27044e435a2b203e32675e942eb8de620ee58 \
    && php -m | grep -oiE '^imagick$' \
    && true
