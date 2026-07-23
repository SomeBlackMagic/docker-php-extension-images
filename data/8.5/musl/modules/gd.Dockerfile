# -------------------- Installing PHP Extension: gd --------------------
RUN set -eux \
#    && apk add libpng libpng-dev libjpeg-turbo libjpeg-turbo-dev \
#    && docker-php-ext-configure gd --with-jpeg=/usr/include/ \
    && install-php-extensions gd \
    && php -m | grep -oiE '^gd$' \
    && php -i | grep -oiE '^FreeType Support => enabled$' \
    && php -i | grep -oiE '^GIF Read Support => enabled$' \
    && php -i | grep -oiE '^JPEG Support => enabled$' \
    && php -i | grep -oiE '^PNG Support => enabled$' \
    && php -i | grep -oiE '^WBMP Support => enabled$' \
    && php -i | grep -oiE '^XPM Support => enabled$' \
    && php -i | grep -oiE '^WebP Support => enabled$' \
    && php -i | grep -oiE '^TGA Read Support => enabled$' \
    && true
