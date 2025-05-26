# -------------------- Installing PHP Extension: imagick --------------------
RUN set -eux \
    && install-php-extensions imagick \
    && php -m | grep -oiE '^imagick$' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'PNG' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'JPEG' \
    && php -r "print_r(Imagick::queryFormats());" | grep 'PDF' \
    && true
