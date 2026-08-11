FROM php:7.4-alpine

RUN set -eux \
    && apk upgrade --available \
    && apk add curl autoconf build-base autoconf automake git gcc make g++  \
    && true

COPY --from=someblackmagic/docker-php-extension-images:7.4-mysqli-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-pdo_mysql-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-propro-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-raphf-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-redis-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-sockets-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-zip-musl / /
COPY --from=someblackmagic/docker-php-extension-images:7.4-http-musl / /

###
### Verify
###
RUN set -eux \
    && echo "date.timezone=UTC" > /usr/local/etc/php/php.ini \
    && php -v | grep -oE 'PHP\s[.0-9]+' | grep -oE '[.0-9]+' | grep '^7.4' \
    \
    && PHP_ERROR="$( php -v 2>&1 1>/dev/null )" \
    && if [ -n "${PHP_ERROR}" ]; then echo "${PHP_ERROR}"; false; fi \
    && PHP_ERROR="$( php -i 2>&1 1>/dev/null )" \
    && if [ -n "${PHP_ERROR}" ]; then echo "${PHP_ERROR}"; false; fi \
    \
    && rm -f /usr/local/etc/php/php.ini \
    && true
