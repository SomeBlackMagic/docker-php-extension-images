#TODO not working
#COPY --from=someblackmagic/docker-php-extension-images:8.3-curl-alpine / /
#COPY --from=someblackmagic/docker-php-extension-images:8.3-sockets-alpine / /
#COPY --from=someblackmagic/docker-php-extension-images:8.3-pgsql-alpine / /
#
#RUN set -eux \
#    && git add . \
#    && git commit -m "deps"
#
#
## -------------------- Installing PHP Extension: swoole --------------------
RUN set -eux \
#    # Installation: Generic
#    # Type:         PECL extension
#    # Custom:       Pecl command  \
#    # test deps ext
#    && php -m | grep -oiE '^curl$' \
#    && php -m | grep -oiE '^sockets$' \
#    \
#    && apk add openssl-dev \
#    && yes yes | pecl install swoole \
#    # Enabling
    && install-php-extensions swoole \
    && php -m | grep -oiE '^swoole$' \
    && true
