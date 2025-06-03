# -------------------- Installing PHP Extension: http --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension
#    && apk add zlib-dev curl-dev icu-dev \
#    && pecl install pecl_http-3.2.4 \
#    && docker-php-ext-enable --ini-name zz-http.ini http \
    && install-php-extensions http \
    && php -m | grep -oiE '^http$' \
    && true


