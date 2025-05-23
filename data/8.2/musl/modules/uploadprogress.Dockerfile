# -------------------- Installing PHP Extension: uploadprogress --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         GIT extension \
    && apk add git \
    && git clone https://github.com/php/pecl-php-uploadprogress /tmp/uploadprogress \
    && cd /tmp/uploadprogress \
    # Default:      Install command
    && phpize \
    && ./configure  --enable-uploadprogress \
    && make -j$(getconf _NPROCESSORS_ONLN) \
    && make install \
    # Enabling
    && docker-php-ext-enable uploadprogress \
    && php -m | grep -oiE '^uploadprogress$' \
    && true
