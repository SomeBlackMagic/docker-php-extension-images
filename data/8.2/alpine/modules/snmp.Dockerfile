# -------------------- Installing PHP Extension: snmp --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         Built-in extension' \
    && apk add net-snmp-dev \
    && docker-php-ext-install -j$(getconf _NPROCESSORS_ONLN) snmp \
    && php -m | grep -oiE '^snmp$' \
    && true
