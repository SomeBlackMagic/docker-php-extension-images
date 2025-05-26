# -------------------- Installing PHP Extension: gd --------------------
RUN set -eux \
    # Installation: Version specific
    # Type:         Built-in extension
    # Custom:       configure command \
    && apk add libpng libpng-dev libjpeg-turbo libjpeg-turbo-dev \
    && docker-php-ext-configure gd --with-jpeg=/usr/include/ \
    # Installation
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) gd \
    && php -m | grep -oiE '^gd$' \
    && true
