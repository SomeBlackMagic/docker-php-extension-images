# -------------------- Installing PHP Extension: ldap --------------------
RUN set -eux \
    # Generic pre-command \
    && apk add ldb-dev libldap openldap-dev \
    # Installation: Generic
    # Type:         Built-in extension
    # Custom:       configure command
    && docker-php-ext-configure ldap --with-ldap --with-ldap-sasl \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) ldap \
    && php -m | grep -oiE '^ldap$' \
    && true
