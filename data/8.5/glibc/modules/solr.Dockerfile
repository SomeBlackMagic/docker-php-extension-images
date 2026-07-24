# -------------------- Installing PHP Extension: solr --------------------
RUN set -eux \
    && install-php-extensions solr \
    && php -m | grep -oiE '^solr$' \
    && true
