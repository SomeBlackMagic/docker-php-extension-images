# -------------------- Installing PHP Extension: ldap --------------------
RUN set -eux \
    && install-php-extensions ldap \
    && php -m | grep -oiE '^ldap$' \
    && true
