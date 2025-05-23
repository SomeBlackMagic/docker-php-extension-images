# -------------------- Installing PHP Extension: snmp --------------------
RUN set -eux \
    && install-php-extensions snmp \
    && php -m | grep -oiE '^snmp$' \
    && true
