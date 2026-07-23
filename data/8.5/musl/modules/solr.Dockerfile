# -------------------- Installing PHP Extension: solr --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command
#    && apk add curl-dev libxml2-dev \
#    && pecl install solr \
    # Enabling
    && install-php-extensions solr \
    && php -m | grep -oiE '^solr$' \
    && true
