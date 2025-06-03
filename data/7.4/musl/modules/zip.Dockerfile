# -------------------- Installing PHP Extension: zip --------------------
RUN set -eux \
    # Installation: Version specific
    # Type:         Built-in extension
    # Custom:       configure command \
#    && apk add libzip-dev bzip2-dev \
#    && docker-php-ext-configure zip --with-zip \
    # Installation
    && install-php-extensions zip \
    && php -m | grep -oiE '^zip$' \
    && true
