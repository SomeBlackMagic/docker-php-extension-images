# -------------------- Installing PHP Extension: imap --------------------
RUN set -eux \
    # Generic pre-command
    # Installation: Generic
    # Type:         Built-in extension
    # Custom:       configure command \
    && apk add imap-dev openssl-dev \
    && docker-php-ext-configure imap --with-imap-ssl --with-imap \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) imap \
    && php -m | grep -oiE '^imap$' \
    && true
