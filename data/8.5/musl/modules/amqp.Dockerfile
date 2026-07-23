# -------------------- Installing PHP Extension: amqp --------------------
RUN set -eux \
    # Installation: Generic
    # Type:         PECL extension
    # Custom:       Pecl command
#    && apk add rabbitmq-c-dev \
#    && echo "/usr" | pecl install amqp \
    # Enabling
    && install-php-extensions amqp \
    && php -m | grep -oiE '^amqp$' \
    && true
