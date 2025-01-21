# -------------------- Installing PHP Extension: memcached --------------------
RUN set -eux \
    # Installation: Version specific
    # Type:         GIT extension \
    && apk add git pkgconfig libmemcached-libs zlib zlib-dev libmemcached-dev cyrus-sasl-dev \
    && git clone https://github.com/php-memcached-dev/php-memcached /tmp/memcached \
    && cd /tmp/memcached \
    # Custom:       Branch
    && git checkout master \
    # Custom:       Install command
    && phpize && ./configure --enable-memcached && make -j$(getconf _NPROCESSORS_ONLN) && make install \
    # Enabling
    && docker-php-ext-enable memcached \
    && php -m | grep -oiE '^memcached$' \
    && true
