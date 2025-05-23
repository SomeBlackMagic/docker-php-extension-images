# -------------------- Installing PHP Extension: rdkafka --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Default:      Pecl command \
    && apk add librdkafka-dev \
    && pecl install rdkafka \
    # Enabling
    && docker-php-ext-enable rdkafka \
    && php -m | grep -oiE '^rdkafka$' \
    && true
