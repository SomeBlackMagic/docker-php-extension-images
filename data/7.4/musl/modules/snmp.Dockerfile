# -------------------- Installing PHP Extension: snmp --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension' \
#    && apk add net-snmp-dev \
    && install-php-extensions snmp \
    && php -m | grep -oiE '^snmp$' \
    && true
