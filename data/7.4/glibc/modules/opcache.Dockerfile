# -------------------- Installing PHP Extension: opcache --------------------
RUN set -eux \
    && install-php-extensions opcache \
    && php -i | grep '^Zend OPcache$' \
    && true
